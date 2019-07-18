#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:03

from __future__ import annotations

import copy
from datetime import datetime
from typing import List, Dict

import requests
from jira import JIRA, Issue

from core.base_classes import Provider, Package
from utils import logger as log
from utils.config import (
    PackageState,
    JiraLane,
    Catalog,
    Present,
    JiraAutopromote,
)
from utils.config import conf
from utils.exceptions import JiraIssueMissingFields

logger = log.get_logger(__file__)


class JiraBoardProvider(Provider):
    """
    Connects to a specific jira server and represents the state of the issues
    in the jira board by showing them as `Package`. It handles changes to the
    packages itself and uploads relevant
    information to the corresponding jira issue.
    """

    def __init__(self, name: str, dry_run: bool = conf.DRY_RUN):
        """
        Initializes a `JiraBoardProvider` object with a given name.

        :param name: `str` Name of the provider
        :param dry_run: `bool` If true, none of the changes will be committed in
        :func:`commit`
        """
        super().__init__(name, dry_run)
        # noinspection PyTypeChecker
        self._jira = None  # type: JIRA

    def connect(self, connection_params=conf.JIRA_CONNECTION_INFO):
        """
        Connects to a jira instance by using the configured connection
        information

        :param connection_params: Parameters to connect to the jira api, if no
        explicit parameters a given it will use
        the values defined in the config.py file
        :return: `bool` True if the connection was successful
        """
        try:
            self._jira = JIRA(**connection_params)

            if self._jira:
                logger.debug("Successfully connected to Jira instance.")
                return True
        except requests.exceptions.ConnectionError as e:
            logger.critical(
                f"Could not connect to Jira instance: "
                f"{connection_params.get('server')}, \n because of {e}."
            )
            return False

    def load(self):
        """
        If a successful connection to the jira instance is possible all issues
        for a given project key are loaded.
        Issues are loaded in batches, if the project has more issues than the
        batch size, the issues are loaded
        continuously.
        After loading the issues, these are converted into a `Package` with
        :func:`_jira_issue_to_package_dict`.
        """
        if self.is_loaded or self.connect():
            query = f"project={conf.JIRA_PROJECT_KEY}"
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
                self._packages_dict = self._jira_issue_to_package_dict(
                    cumulative_results
                )
                return

            self._packages_dict = self._jira_issue_to_package_dict(
                search_result
            )

    @staticmethod
    def check_jira_issue_exists(package: Package) -> bool:
        """
        Checks whether a given package already exists in the Jira Board or not.

        :param package: The package to check whether it exists in Jira.
        :return: `True` if the package has a Jira ID and `False` if not
        """
        return bool(package.jira_id)

    def _jira_issue_to_package_dict(self, issues: List[Issue]) -> Dict:
        """
        Wrapper method around the :func:`_jira_issue_to_package` method which
        handles a list of `Issue`.

        :param issues: `List` containing `Issue` to be converted to `Package`
        objects
        :return: `Dict` containing the newly created `Package` objects
        """
        packages = dict()
        for issue in issues:
            p = self._jira_issue_to_package(issue)
            packages.update({p.key: p})

        return packages

    def _jira_issue_to_package(self, issue: Issue) -> Package:
        """
        Converts a given issue into a `Package` object. Before converting the
        issue is verified to contain
        all needed fields. In case the package is missing certain fields defined
        in `conf.ISSUE_FIELDS`,
        `JiraIssueMissingFields` is raised.

        :param issue: The jira issue converted to a `Package`
        :return: `Package` representing the issue
        """
        fields_dict = issue.fields.__dict__  # type: dict

        if all(field in fields_dict for field in conf.ISSUE_FIELDS):
            # Before we try to get all fields from our issue we check, whether
            # all fields are present as keys

            if fields_dict.get(conf.JIRA_PRESENT_FIELD):
                is_present = Present(
                    fields_dict.get(conf.JIRA_PRESENT_FIELD)[0].id
                )
            else:
                is_present = Present(None)

            p = Package(
                name=fields_dict.get(conf.JIRA_SOFTWARE_NAME_FIELD),
                version=Package.str_to_version(
                    fields_dict.get(conf.JIRA_SOFTWARE_VERSION_FIELD)
                ),
                catalog=Catalog(fields_dict.get(conf.JIRA_CATALOG_FIELD).id),
                promote_date=datetime.strptime(
                    fields_dict.get(conf.JIRA_DUEDATE_FIELD), "%Y-%m-%d"
                ),
                is_autopromote=JiraAutopromote(
                    fields_dict.get(conf.JIRA_AUTOPROMOTE_FIELD).id
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
        """
        Searches for a package in jira and updates it according to the package
        given in the argument.
        If no jira issue exists matching the given package it is created.

        To prevent `PackageState` changes in propagating to other `Provider`
        instances a deepcopy is created at the
        beginning of the method.

        In case the package already exists we can check if we need to update
        certain values. In this case the
        `PackageState` is set to `PackageState.UPDATE`.

        Otherwise if we want to create a new one the state is set to
        `PackageState.NEW`.

        :param package: `Package` object to be written to jira
        """
        package = copy.deepcopy(package)
        if JiraBoardProvider.check_jira_issue_exists(package):
            # Ticket with this id already exists.
            p = self._packages_dict.get(package.key)

            for key, value in package.__dict__.items():
                if p.__dict__.get(key) != value:
                    # Not all values of the existing jira ticket and the local
                    # version match. Therefore update.
                    p.state = PackageState.UPDATE
                    # Replace original package with updated package
                    self._packages_dict.update({p.key: package})
                    return
            logger.debug(
                f"Jira update called for {package}, but no changes detected."
            )
        else:
            package.state = PackageState.NEW
            if package.key not in self._packages_dict:
                logger.debug(f"Creating new jira ticket for {package}")
                self._packages_dict.update({package.key: package})

    def commit(self) -> bool:
        """
        Checks if the program runs as a dry run and if this is not the case, all
        previously made changes
        are committed to jira.
        :return: `bool` True if the run was not a dry run and changes were
        committed.
        """
        if not self._dry_run:
            for package in self.get().values():

                issue_dict = {
                    conf.JIRA_SOFTWARE_NAME_FIELD: package.name,
                    conf.JIRA_SOFTWARE_VERSION_FIELD: str(package.version),
                    conf.JIRA_DUEDATE_FIELD: package.promote_date.strftime(
                        "%Y-%m-%d"
                    ),
                    conf.JIRA_DESCRIPTION_FIELD: package.name,
                    conf.JIRA_CATALOG_FIELD: package.catalog.to_jira_rest_dict(),
                    conf.JIRA_AUTOPROMOTE_FIELD:
                        package.is_autopromote.to_jira_rest_dict(),
                    conf.JIRA_PRESENT_FIELD: [
                        package.is_present.to_jira_rest_dict()
                    ],
                }

                if package.state == PackageState.NEW:
                    # Create a new ticket.
                    # Add the required fields we need to create a new ticket
                    # compared to an update call.
                    issue_dict.update(
                        {
                            conf.JIRA_PROJECT_FIELD: conf.JIRA_PROJECT_KEY,
                            conf.JIRA_ISSUE_TYPE_FIELD: conf.JIRA_ISSUE_TYPE,
                            conf.JIRA_SUMMARY_FIELD: package.key,
                        }
                    )

                    logger.debug(f"Creating new ticket for package {package}")

                    created_ticket = self._jira.create_issue(fields=issue_dict)
                    current_ticket_lane = JiraLane(
                        created_ticket.fields.__dict__.get("status").name
                    )
                    if current_ticket_lane != package.jira_lane:
                        self._jira.transition_issue(
                            created_ticket, package.catalog.transition_id
                        )

                elif package.state == PackageState.UPDATE:
                    # Update package information
                    existing_ticket = self._jira.search_issues(
                        f"project={conf.JIRA_PROJECT_KEY} AND "
                        f"key={package.jira_id} "
                    )[
                        0
                    ]  # type: Issue

                    logger.debug(f"Updating ticket for package {package}")

                    existing_ticket.update(fields=issue_dict)
                    current_ticket_lane = JiraLane(
                        existing_ticket.fields.__dict__.get("status").name
                    )
                    if current_ticket_lane != package.jira_lane:
                        self._jira.transition_issue(
                            existing_ticket, package.catalog.transition_id
                        )
            return True

        return False

    def update_jira_from_repo(self, munki_packages: Dict):
        """
        Updates the jira board based on the munki packages in two ways.
        If a package exists in munki, but not in jira, then a issue is created.
        If a issue exists in jira which is specified to be missing in munki, but
        it was added to munki,
        then the missing attribute of jira is set to not missing.

        :param munki_packages: `Dict` of all munki packages
        """
        for munki_key, munki_package in munki_packages.items():
            munki_package = copy.deepcopy(munki_package)
            if not self._get(munki_key):
                logger.debug(f"Adding munki package {munki_package} to jira.")
                munki_package.state = PackageState.NEW
                self._packages_dict.update({munki_key: munki_package})
                continue

            existing_issue = self._get(munki_key)
            if existing_issue.is_present == Present.MISSING:
                existing_issue.is_present = Present.PRESENT
                existing_issue.state = PackageState.UPDATE
