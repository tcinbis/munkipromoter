import os
from enum import Enum, auto
from logging import DEBUG


class JiraLane(Enum):
    TO_DEVELOPMENT = "to_dev"
    DEVELOPMENT = "dev"
    TO_TESTING = "to_test"
    TESTING = "test"
    TO_PRODUCTION = "to_prod"
    PRODUCTION = "prod"


class Catalog(Enum):
    DEVELOPMENT = {"id": "12000"}
    TESTING = {"id": "12001"}
    PRODUCTION = {"id": "12002"}


class Present(Enum):
    PRESENT = {"id": "12005"}
    MISSING = {"id": "12006"}


class PackageState(Enum):
    DEFAULT = auto()
    NEW = auto()
    UPDATE = auto()
    MISSING = auto()


REPO_PATH = os.getenv("MUNKIPROMOTER_REPO_PATH", "/Volumes/munki_repo")
CATALOGS_PATH = os.getenv("MUNKIPROMOTER_CATALOGS_PATH", f"{REPO_PATH}/catalogs")
PKGS_INFO_PATH = os.getenv("MUNKIPROMOTER_PKGS_INFO_PATH", f"{REPO_PATH}/pkgsinfo")
MAKECATALOGS_PATH = os.getenv("MUNKIPROMOTER_MAKECATALOGS_PATH", "/usr/local/munki")

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
JIRA_LABELS_FIELD = "labels-textarea"
JIRA_CATALOG_FIELD = os.getenv("MUNKIPROMOTER_JIRA_CATALOG_FIELD", "customfield_12700")
JIRA_AUTOPROMOTE_FIELD = os.getenv(
    "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FIELD", "customfield_12701"
)

__JIRA_AUTOPROMOTE_TRUE = os.getenv("MUNKIPROMOTER_JIRA_AUTOPROMOTE_TRUE", "12003")
__JIRA_AUTOPROMOTE_FALSE = os.getenv("MUNKIPROMOTER_JIRA_AUTOPROMOTE_FALSE", "12004")

JIRA_AUTOPROMOTE = dict(
    {True: {"id": __JIRA_AUTOPROMOTE_TRUE}, False: {"id": __JIRA_AUTOPROMOTE_FALSE}}
)

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

LOG_LEVEL = DEBUG
LOG_DIR = os.getenv("MUNKIPROMOTER_LOG_DIR", "/var/log")
LOG_MAIL = os.getenv("MUNKIPROMOTER_LOG_MAIL", "tom.cinbis@unibas.ch")
