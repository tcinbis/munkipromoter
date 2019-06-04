from __future__ import annotations
import os
from enum import Enum, auto

REPO_PATH = os.getenv("MUNKIPROMOTER_REPO_PATH", "/Volumes/munki_repo")
CATALOGS_PATH = os.getenv("MUNKIPROMOTER_CATALOGS_PATH", f"{REPO_PATH}/catalogs")
PKGS_INFO_PATH = os.getenv("MUNKIPROMOTER_PKGS_INFO_PATH", f"{REPO_PATH}/pkgsinfo")
MAKECATALOGS_PATH = os.getenv("MUNKIPROMOTER_MAKECATALOGS_PATH", "/usr/local/munki")

PROMOTE_AFTER_DAYS = 7

# Store Jira connection information in a dict. We can then create a connection by invoking JIRA(**JIRA_CONNECTION_INFO)
JIRA_CONNECTION_INFO = {
    "server": os.getenv("MUNKIPROMOTER_REPO_PATH", "***REMOVED***"),
    "basic_auth": (
        os.getenv("MUNKIPROMOTER_JIRA_USER", "***REMOVED***"),
        os.getenv("MUNKIPROMOTER_JIRA_PASSWORD", "***REMOVED***"),
    ),
}

JIRA_PROJECT_KEY = os.getenv("MUNKIPROMOTER_JIRA_PROJECT_KEY", "SWPM")
JIRA_ISSUE_TYPE = os.getenv("MUNKIPROMOTER_JIRA_ISSUE_TYPE", "Story")

JIRA_SOFTWARE_NAME_FIELD = os.getenv(
    "MUNKIPROMOTER_JIRA_SOFTWARE_NAME_FIELD", "customfield_12503"
)
JIRA_PROJECT_FIELD = "project"
JIRA_ISSUE_TYPE_FIELD = "issuetype"
JIRA_SUMMARY_FIELD = "summary"
JIRA_DESCRIPTION_FIELD = "description"
JIRA_SOFTWARE_VERSION_FIELD = os.getenv(
    "MUNKIPROMOTER_JIRA_SOFTWARE_VERSION_FIELD", "customfield_12504"
)
JIRA_DUEDATE_FIELD = "duedate"
JIRA_LABELS_FIELD = "labels"
JIRA_CATALOG_FIELD = os.getenv("MUNKIPROMOTER_JIRA_CATALOG_FIELD", "customfield_12700")
JIRA_AUTOPROMOTE_FIELD = os.getenv(
    "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FIELD", "customfield_12701"
)

_JIRA_AUTOPROMOTE_TRUE = os.getenv("MUNKIPROMOTER_JIRA_AUTOPROMOTE_TRUE", "12003")
_JIRA_AUTOPROMOTE_FALSE = os.getenv("MUNKIPROMOTER_JIRA_AUTOPROMOTE_FALSE", "12004")

JIRA_PRESENT_FIELD = os.getenv("MUNKIPROMOTER_JIRA_PRESENT_FIELD", "customfield_12702")

ISSUE_FIELDS = [
    JIRA_SOFTWARE_NAME_FIELD,
    JIRA_SOFTWARE_VERSION_FIELD,
    JIRA_DUEDATE_FIELD,
    JIRA_DESCRIPTION_FIELD,
    JIRA_LABELS_FIELD,
    JIRA_CATALOG_FIELD,
    JIRA_AUTOPROMOTE_FIELD,
    JIRA_PRESENT_FIELD,
]

DEFAULT_PROMOTION_INTERVAL = os.getenv("MUNKIPROMOTER_DEFAULT_PROMOTION_INTERVAL", 4)
DEFAULT_PROMOTION_DAY = os.getenv("MUNKIPROMOTER_DEFAULT_PROMOTION_DAY", "Thursday")

LOG_LEVEL = os.getenv("MUNKIPROMOTER_LOG_LEVEL", "DEBUG")
LOG_BACKUP_COUNT = os.getenv("MUNKIPROMOTER_LOG_BACKUP_COUNT", 3)
LOG_DIR = os.getenv("MUNKIPROMOTER_LOG_DIR", "/var/log")
LOG_MAIL = os.getenv("MUNKIPROMOTER_LOG_MAIL", "tom.cinbis@unibas.ch")


class JiraEnum(Enum):
    def to_jira_rest_dict(self):
        """
        When submitting a field to the Jira API it usually requires a dictionary with a  key called id and the
        corresponding value of this id. This method simply returns a dict with such key and the value stored in the
        enum instance.
        :return: Dictionary with id key and id value.
        """
        return {"id": self.value}


class JiraLane(JiraEnum):
    # TODO: Replace with ids
    TO_DEVELOPMENT = "To Development"
    DEVELOPMENT = "Development"
    TO_TESTING = "To Testing"
    TESTING = "Testing"
    TO_PRODUCTION = "To Production"
    PRODUCTION = "Production"

    @staticmethod
    def catalog_to_lane(catalog: Catalog) -> JiraLane:
        for j_enum in JiraLane:
            if j_enum.name == catalog.name:
                return j_enum


class Catalog(JiraEnum):
    DEVELOPMENT = "12000"
    TESTING = "12001"
    PRODUCTION = "12002"

    @staticmethod
    def str_to_catalog(catalog_string: str) -> Catalog:
        catalog_string = (
            catalog_string.upper()
        )  # in case the string is not already all upper case we will do it here
        for c_enum in Catalog:
            if c_enum.name == catalog_string:
                return c_enum


class Present(JiraEnum):
    PRESENT = "12005"
    MISSING = "12006"


class PackageState(JiraEnum):
    DEFAULT = auto()
    NEW = auto()
    UPDATE = auto()
    MISSING = auto()


class JiraAutopromote(JiraEnum):
    PROMOTE = _JIRA_AUTOPROMOTE_TRUE
    NOPROMOTE = _JIRA_AUTOPROMOTE_FALSE

    def __bool__(self):
        if self.name == self.PROMOTE.name:
            return True
        else:
            return False
