from __future__ import annotations

import os
from enum import Enum, auto


class MunkiPromoterConfig:
    """
    This class stores all relevant configuration and will try to load them from the local environment, before falling
    back to the predefined default values.
    As the class is supposed to be consistent throughout the project the singleton pattern is used to ensure only one
    instance with the same information exists.
    """

    class __MunkiPromoterConfig:
        REPO_PATH = os.getenv("MUNKIPROMOTER_REPO_PATH", "/Volumes/munki_repo_test")
        CATALOGS_PATH = os.getenv(
            "MUNKIPROMOTER_CATALOGS_PATH", f"{REPO_PATH}/catalogs"
        )
        PKGS_INFO_PATH = os.getenv(
            "MUNKIPROMOTER_PKGS_INFO_PATH", f"{REPO_PATH}/pkgsinfo"
        )
        DEBUG_PKGS_INFO_SAVE_PATH = os.getenv(
            "MUNKIPROMOTER_DEBUG_PKGS_INFO_SAVE_PATH", None
        )
        MAKECATALOGS = os.getenv(
            "MUNKIPROMOTER_MAKECATALOGS", "/usr/local/munki/makecatalogs"
        )

        # Store Jira connection information in a dict. We can then create a connection by invoking JIRA(**JIRA_CONNECTION_INFO)
        JIRA_CONNECTION_INFO = {
            "server": os.getenv(
                "MUNKIPROMOTER_REPO_PATH", "https://deployment-jira.its.unibas.ch"
            ),
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
        JIRA_CATALOG_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_CATALOG_FIELD", "customfield_12703"
        )
        JIRA_AUTOPROMOTE_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FIELD", "customfield_12701"
        )

        _JIRA_AUTOPROMOTE_TRUE = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_TRUE", "12003"
        )
        _JIRA_AUTOPROMOTE_FALSE = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FALSE", "12004"
        )

        JIRA_PRESENT_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_PRESENT_FIELD", "customfield_12704"
        )

        JIRA_DEVELOPMENT_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_DEVELOPMENT_TRANSITION_NAME", "all to development"
        )
        JIRA_TESTING_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_TESTING_TRANSITION_NAME", "all to test"
        )
        JIRA_PRODUCTION_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_PRODUCTION_TRANSITION_NAME", "all to prod"
        )

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

        DEFAULT_PROMOTION_INTERVAL = os.getenv(
            "MUNKIPROMOTER_DEFAULT_PROMOTION_INTERVAL", 7
        )
        DEFAULT_PROMOTION_DAY = os.getenv(
            "MUNKIPROMOTER_DEFAULT_PROMOTION_DAY", "Thursday"
        )

        LOG_LEVEL = os.getenv("MUNKIPROMOTER_LOG_LEVEL", "DEBUG")
        LOG_BACKUP_COUNT = os.getenv("MUNKIPROMOTER_LOG_BACKUP_COUNT", 3)
        LOG_DIR = os.getenv("MUNKIPROMOTER_LOG_DIR", "/var/log")
        LOG_MAIL = os.getenv("MUNKIPROMOTER_LOG_MAIL", "tom.cinbis@unibas.ch")

    instance = None

    def __init__(self):
        if not MunkiPromoterConfig.instance:
            MunkiPromoterConfig.instance = MunkiPromoterConfig.__MunkiPromoterConfig()

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        setattr(self.instance, key, value)


conf = MunkiPromoterConfig()


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

    @property
    def is_promotion_lane(self):
        if "TO" in self.name:
            return True
        return False


class Catalog(JiraEnum):
    DEVELOPMENT = "12007"
    TESTING = "12008"
    PRODUCTION = "12009"

    @staticmethod
    def str_to_catalog(catalog_string: str) -> Catalog:
        catalog_string = (
            catalog_string.upper()
        )  # in case the string is not already all upper case we will do it here
        for c_enum in Catalog:
            if c_enum.name == catalog_string:
                return c_enum

    @staticmethod
    def jira_lane_to_catalog(jira_lane: JiraLane) -> Catalog:
        return Catalog.str_to_catalog(jira_lane.name.replace("TO_", ""))

    @property
    def next_catalog(self) -> Catalog:
        catalog_order = {
            0: Catalog.DEVELOPMENT,
            1: Catalog.TESTING,
            2: Catalog.PRODUCTION,
        }
        inv_catalog_order = {v: k for k, v in catalog_order.items()}

        new_catalog = catalog_order.get(inv_catalog_order.get(self) + 1)
        return (
            new_catalog if new_catalog else self
        )  # in case we get a catalog like prod there is no next catalog

    @property
    def transition_id(self) -> str:
        transition_dict = {
            Catalog.DEVELOPMENT: conf.JIRA_DEVELOPMENT_TRANSITION_NAME,
            Catalog.TESTING: conf.JIRA_TESTING_TRANSITION_NAME,
            Catalog.PRODUCTION: conf.JIRA_PRODUCTION_TRANSITION_NAME,
        }

        return transition_dict.get(self)


class Present(JiraEnum):
    PRESENT = "12010"
    MISSING = None


class PackageState(JiraEnum):
    DEFAULT = auto()
    NEW = auto()
    UPDATE = auto()


class JiraAutopromote(JiraEnum):
    PROMOTE = conf._JIRA_AUTOPROMOTE_TRUE
    NOPROMOTE = conf._JIRA_AUTOPROMOTE_FALSE

    def __bool__(self):
        if self.name == self.PROMOTE.name:
            return True
        else:
            return False
