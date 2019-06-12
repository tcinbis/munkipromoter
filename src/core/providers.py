from __future__ import annotations

import os
import plistlib
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict
from uuid import uuid4

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
    PKGS_INFO_PATH,
    DEBUG_PKGS_INFO_SAVE_PATH,
    MAKECATALOGS,
)
from utils.exceptions import (
    ProviderDoesNotImplement,
    JiraIssueMissingFields,
    MunkiItemInMultipleCatalogs,
)

logger = l.get_logger(__file__)


class MunkiRepoProvider(Provider):
    def __init__(self, name, dry_run=False):
        super().__init__(name, dry_run)
        self._pkg_info_files = dict(dict())

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

    def _load_packages(self):
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
                            provider=MunkiRepoProvider,
                            jira_id=None,
                            jira_lane=JiraLane.catalog_to_lane(item_catalog),
                            state=PackageState.DEFAULT,
                            munki_uuid=uuid4(),
                        )

                        self._packages_dict.update({p.munki_uuid: p})
                    except MunkiItemInMultipleCatalogs as e:
                        logger.error(e)

    def _load_pkg_infos(self):
        for dirpath, dirnames, filenames in os.walk(PKGS_INFO_PATH):
            for file in filenames:
                if file.startswith("."):
                    continue

                pkg_info_path = os.path.join(dirpath, file)
                pkg_info = plistlib.load(open(pkg_info_path, "rb"))

                # at index 0 we store the actual plist and at index 1 the path to that plist file is stored.
                d = {pkg_info.get("version"): (pkg_info, pkg_info_path)}

                if self._pkg_info_files.get(pkg_info.get("name")):
                    # pkg info files with this name already stored -> update
                    self._pkg_info_files.get(pkg_info.get("name")).update(d)
                else:
                    # no pkg info files with this name already stored -> add
                    self._pkg_info_files.update({pkg_info.get("name"): d})

    def load(self):
        self._load_packages()
        self._load_pkg_infos()
        self.is_loaded = True

    def update(self, package: Package):
        if package.provider == MunkiRepoProvider:
            # Ticket was originally created by MunkiRepoProvider.
            # Therefore must already exist and we only need to update.
            p = self._packages_dict.get(package.munki_uuid)
            if p.munki_uuid == package.munki_uuid:
                for key, value in package.__dict__.items():
                    if p.__dict__.get(key) != value:
                        # Not all values of the existing jira ticket and the local version match. Therefore update.
                        package.state = PackageState.UPDATE
                        self._packages_dict.update({package.munki_uuid: package})
                        break
        elif package.provider == JiraBoardProvider:
            raise ProviderDoesNotImplement()
            package.state = PackageState.NEW
            if package not in self._packages_dict:
                self._packages_dict.update({package.munki_uuid: package})

    def commit(self) -> bool:
        if not self._dry_run:
            for package in self._packages_dict.values():
                if package.state == PackageState.UPDATE:
                    pkg_info, pkg_info_path = self._pkg_info_files.get(
                        package.name
                    ).get(package.version)

                    if pkg_info:
                        # Plist already exists in Repo so we can continue to update it.
                        pkg_info.update({"catalogs": [package.catalog.name.lower()]})

                        f = open(
                            os.path.join(
                                DEBUG_PKGS_INFO_SAVE_PATH,
                                os.path.basename(pkg_info_path),
                            )
                            if DEBUG_PKGS_INFO_SAVE_PATH
                            else pkg_info_path,
                            "wb",
                        )
                        plistlib.dump(pkg_info, f)
                        logger.debug(f"Wrote pkg info file at {f.name}")
                    else:
                        # Plist does not exist in Repo, and we can not create a new one.
                        package.state = PackageState.MISSING
                        logger.debug(
                            f"{package} is missing in {self.name} {self.__class__.__name__}"
                        )
                        continue
                elif package.state == PackageState.NEW:
                    logger.debug(
                        f"Pkg info for {package} not written, because package state is {package.state}"
                    )

            MunkiRepoProvider.make_catalogs()
            return True
        return False

    @staticmethod
    def make_catalogs():
        """
        Run makecatalogs and check whether the return code is 0.
        """
        cmd = [MAKECATALOGS, REPO_PATH]
        logger.info("Running makecatalogs.")
        subprocess.run(cmd, check=True)
        logger.info("Makecatalogs completed.")


class JiraBoardProvider(Provider):
    def __init__(self, name, dry_run=False):
        super().__init__(name, dry_run)
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
            self._packages_dict = self._jira_issue_to_package_dict(cumulative_results)
            return

        self._packages_dict = self._jira_issue_to_package_dict(search_result)

    @staticmethod
    def check_jira_issue_exists(package: Package) -> bool:
        """
        Checks whether a given package already exists in the Jira Board or not.
        :param package: The package to check whether it exists in Jira.
        :return: True if the package has a Jira ID and False if not
        """
        return bool(package.jira_id)

    def _jira_issue_to_package_dict(self, issues: List[Issue]) -> Dict:
        packages = dict()
        for issue in issues:
            p = self._jira_issue_to_package(issue)
            packages.update({p.jira_id: p})

        return packages

    def _jira_issue_to_package(self, issue: Issue) -> "Package":
        fields_dict = issue.fields.__dict__  # type: dict

        if all(field in fields_dict for field in ISSUE_FIELDS):
            # Before we try to get all fields from our issue we check, whether all fields are present as keys

            if fields_dict.get(JIRA_PRESENT_FIELD):
                is_present = Present(fields_dict.get(JIRA_PRESENT_FIELD)[0].id)
            else:
                is_present = Present(None)

            p = Package(
                name=fields_dict.get(JIRA_SOFTWARE_NAME_FIELD),
                version=Package.str_to_version(
                    fields_dict.get(JIRA_SOFTWARE_VERSION_FIELD)
                ),
                catalog=Catalog(fields_dict.get(JIRA_CATALOG_FIELD).id),
                date=datetime.strptime(fields_dict.get(JIRA_DUEDATE_FIELD), "%Y-%m-%d"),
                is_autopromote=JiraAutopromote(
                    fields_dict.get(JIRA_AUTOPROMOTE_FIELD).id
                ),
                is_present=is_present,
                provider=JiraBoardProvider,
                jira_id=issue.key,
                jira_lane=JiraLane(fields_dict.get("status").name),
                state=PackageState.DEFAULT,
                munki_uuid=None,
            )
            return p
        else:
            raise JiraIssueMissingFields()

    def update(self, package: Package):
        if JiraBoardProvider.check_jira_issue_exists(package):
            # Ticket with this id already exists.
            p = self._packages_dict.get(package.jira_id)

            for key, value in package.__dict__.items():
                if p.__dict__.get(key) != value:
                    # Not all values of the existing jira ticket and the local version match. Therefore update.
                    package.state = PackageState.UPDATE
                    # Replace original package with updated package
                    self._packages_dict.update({p.jira_id: package})
                    break
        else:
            package.state = PackageState.NEW
            if package not in self._packages_dict:
                self._packages_dict.update({package.jira_id, package})

    def commit(self) -> bool:
        if not self._dry_run:
            for package in self._packages_dict.values():

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

                if package.state == PackageState.NEW:
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

                elif package.state == PackageState.UPDATE:
                    # Update package information
                    existing_ticket = self._jira.search_issues(
                        f"project={JIRA_PROJECT_KEY} AND key={package.jira_id} "
                    )[
                        0
                    ]  # type: Issue

                    existing_ticket.update(fields=issue_dict)
            return True

        return False
