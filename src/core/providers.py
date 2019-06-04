from __future__ import annotations
import os
import plistlib
from datetime import datetime, timedelta
from typing import List

import requests
from core.base_classes import Provider, Package
from jira import JIRA, Issue
from utils import logger as l
from utils.config import (
    JIRA_PROJECT_FIELD,
    JIRA_PROJECT_KEY,
    JIRA_ISSUE_TYPE,
    JIRA_ISSUE_TYPE_FIELD,
    JIRA_SOFTWARE_NAME_FIELD,
    JIRA_SOFTWARE_VERSION_FIELD,
    JIRA_DUEDATE_FIELD,
    JIRA_DESCRIPTION_FIELD,
    JIRA_CATALOG_FIELD,
    JIRA_AUTOPROMOTE_FIELD,
    JIRA_PRESENT_FIELD,
    JIRA_CONNECTION_INFO,
    JIRA_SUMMARY_FIELD,
    ISSUE_FIELDS,
    PackageState,
    JiraLane,
    Catalog,
    Present,
    JiraAutopromote,
    REPO_PATH,
    CATALOGS_PATH,
    PROMOTE_AFTER_DAYS,
)
from utils.exceptions import (
    ProviderDoesNotImplement,
    JiraIssueMissingFields,
    MunkiItemInMultipleCatalogs,
)

logger = l.get_logger(__file__)


class MunkiRepoProvider(Provider):
    def __init__(self, name):
        super().__init__(name)

    def connect(self):
        """
        The munki repository needs to be mounted when trying to connect.
        """
        if os.path.ismount(REPO_PATH):
            logger.debug(f"Repo at {REPO_PATH} mounted.")
            return True
        else:
            logger.critical(f"Repo mount point {REPO_PATH} not mounted.")
            return False

    def load(self):
        for filename in os.listdir(CATALOGS_PATH):
            if not (filename.startswith(".") or filename == "all"):
                # Ignore hidden files
                munki_packages = plistlib.load(
                    open(os.path.join(CATALOGS_PATH, filename), "rb")
                )

                for item in munki_packages:
                    try:
                        if "promotion_date" in item:
                            promotion_date = item.get("date")
                        else:
                            promotion_date = datetime.now() + timedelta(
                                days=PROMOTE_AFTER_DAYS
                            )

                        if len(item.get("catalogs")) > 1:
                            raise MunkiItemInMultipleCatalogs(item)
                        else:
                            item_catalog = Catalog.str_to_catalog(
                                item.get("catalogs")[0]
                            )
                        # TODO: Check if promotion date in pkginfo plist
                        p = Package(
                            name=item.get("name"),
                            version=item.get("version"),
                            catalog=item_catalog,
                            date=promotion_date,
                            is_autopromote=JiraAutopromote.PROMOTE,
                            is_present=Present.PRESENT,
                            provider=self,
                            jira_id=None,
                            jira_lane=JiraLane.catalog_to_lane(item_catalog),
                            state=PackageState.DEFAULT,
                        )

                        self._packages.append(p)
                    except MunkiItemInMultipleCatalogs as e:
                        logger.error(e)

    def update(self, package: Package):
        raise ProviderDoesNotImplement(self.__class__.__name__)


class JiraBoardProvider(Provider):
    def __init__(self, name):
        super().__init__(name)
        # noinspection PyTypeChecker
        self._jira = None  # type: JIRA

    def connect(self, connection_params=JIRA_CONNECTION_INFO):
        try:
            self._jira = JIRA(**connection_params)

            if self._jira:
                logger.debug("Successfully connected to Jira instance.")
                return True
        except requests.exceptions.ConnectionError as e:
            logger.critical(
                f"Couldn't connect to Jira instance: {JIRA_CONNECTION_INFO.get('server')}."
            )
            return False

    def load(self):
        query = f"project={JIRA_PROJECT_KEY}"
        search_result = self._jira.search_issues(query, maxResults=500)
        total_issues = search_result.total
        self.is_loaded = True

        if total_issues != len(search_result):
            # we could only fetch some tickets and need to fetch more
            logger.debug("Fetching remaining Jira Tickets.")
            cumulative_results = list()

            while len(cumulative_results) != total_issues:
                cumulative_results.extend(search_result.iterable)
                start_at = search_result.startAt + len(search_result)
                search_result.clear()
                search_result = self._jira.search_issues(
                    query, startAt=start_at, maxResults=500
                )
            self._packages = self._jira_issue_to_package_list(cumulative_results)
            return

        self._packages = self._jira_issue_to_package_list(search_result)

    @staticmethod
    def check_jira_issue_exists(package: Package) -> bool:
        """
        Checks whether a given package already exists in the Jira Board or not.
        :param package: The package to check whether it exists in Jira.
        :return: True if the package has a Jira ID and False if not
        """
        return bool(package.jira_id)

    def _jira_issue_to_package_list(self, issues: List[Issue]) -> List[Package]:
        packages = list()
        for issue in issues:
            packages.append(self._jira_issue_to_package(issue))

        return packages

    def _jira_issue_to_package(self, issue: Issue) -> "Package":
        fields_dict = issue.fields.__dict__  # type: dict

        if all(field in fields_dict for field in ISSUE_FIELDS):
            # Before we try to get all fields from our issue we check, whether all fields are present as keys
            p = Package(
                name=fields_dict.get(JIRA_SOFTWARE_NAME_FIELD),
                version=Package.str_to_version(
                    fields_dict.get(JIRA_SOFTWARE_VERSION_FIELD)
                ),
                # TODO: Remove index 0 as catalog field will be changed to RadioSelect
                catalog=Catalog(fields_dict.get(JIRA_CATALOG_FIELD)[0].id),
                date=datetime.strptime(fields_dict.get(JIRA_DUEDATE_FIELD), "%Y-%m-%d"),
                is_autopromote=JiraAutopromote(
                    fields_dict.get(JIRA_AUTOPROMOTE_FIELD).id
                ),
                # TODO: Remove index 0 as present field will be changed to RadioSelect
                is_present=Present(fields_dict.get(JIRA_PRESENT_FIELD)[0].id),
                provider=self,
                jira_id=issue.key,
                jira_lane=JiraLane(fields_dict.get("status").name),
                state=PackageState.DEFAULT,
            )
            return p
        else:
            raise JiraIssueMissingFields()

    def update(self, package: Package):
        issue_dict = {
            # TODO: Add/Set status
            # TODO: Add/Set Package State
            JIRA_SOFTWARE_NAME_FIELD: package.name,
            JIRA_SOFTWARE_VERSION_FIELD: package.version.vstring,
            JIRA_DUEDATE_FIELD: package.date.strftime("%Y-%m-%d"),
            JIRA_DESCRIPTION_FIELD: package.name,
            JIRA_CATALOG_FIELD: [package.catalog.to_jira_rest_dict()],
            JIRA_AUTOPROMOTE_FIELD: package.is_autopromote.to_jira_rest_dict(),
            JIRA_PRESENT_FIELD: [package.is_present.to_jira_rest_dict()],
        }

        if JiraBoardProvider.check_jira_issue_exists(package):
            # Ticket with this id already exists.
            existing_ticket = self._jira.search_issues(
                f"project={JIRA_PROJECT_KEY} AND key={package.jira_id} "
            )[
                0
            ]  # type: Issue

            existing_package = self._jira_issue_to_package(existing_ticket)

            for key, value in package.__dict__.items():
                if existing_package.__dict__.get(key) != value:
                    # Not all values of the existing jira ticket and the local version match. Therefore update.
                    existing_ticket.update(fields=issue_dict)
                    break
        else:
            # Create a new ticket.
            # Add the required fields we need to create a new ticket compared to an update call.
            issue_dict.update(
                {
                    JIRA_PROJECT_FIELD: JIRA_PROJECT_KEY,
                    JIRA_ISSUE_TYPE_FIELD: JIRA_ISSUE_TYPE,
                    JIRA_SUMMARY_FIELD: str(package),
                }
            )
            self._jira.create_issue(fields=issue_dict)
