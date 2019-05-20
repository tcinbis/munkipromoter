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
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class PackageState(Enum):
    NEW = auto()
    UPDATE = auto()
    MISSING = auto()


REPO_PATH = os.getenv("MUNKIPROMOTER_REPO_PATH", "/Volumes/munki_repo")
CATALOGS_PATH = os.getenv("MUNKIPROMOTER_CATALOGS_PATH", f"{REPO_PATH}/catalogs")
PKGS_INFO_PATH = os.getenv("MUNKIPROMOTER_PKGS_INFO_PATH", f"{REPO_PATH}/pkgsinfo")
MAKECATALOGS_PATH = os.getenv("MUNKIPROMOTER_MAKECATALOGS_PATH", "/usr/local/munki")

# Store Jira connection information in a dict. We can then create a connection by invoking JIRA(**JIRA_CONNECTION_INFO)
JIRA_CONNECTION_INFO = {
    "server": os.getenv("MUNKIPROMOTER_REPO_PATH", "https://your-jira-server.com"),
    "basic_auth": (
        os.getenv("MUNKIPROMOTER_JIRA_USER", "user"),
        os.getenv("MUNKIPROMOTER_JIRA_PASSWORD", "password"),
    ),
}

LOG_LEVEL = DEBUG
LOG_DIR = os.getenv("MUNKIPROMOTER_LOG_DIR", "/var/log")
LOG_MAIL = os.getenv("MUNKIPROMOTER_LOG_MAIL", "your_mail@example.com")
