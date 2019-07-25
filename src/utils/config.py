#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

from __future__ import annotations

import configparser
import os
import sys
from enum import Enum, auto
from typing import Any

config_from_file = configparser.ConfigParser(
    interpolation=configparser.ExtendedInterpolation()
)
config_from_file.read(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "default.ini")
)


class ConfigSections(Enum):
    PROMOTION = "Promotion"
    MUNKI = "Munki"
    JIRA = "Jira"
    LOGGER = "Logger"


class MunkiPromoterConfig:
    """
    This class stores all relevant configuration and will try to load them from
    the local environment, before falling back to the predefined default values.
    As the class is supposed to be consistent throughout the project the
    singleton pattern is used to ensure only one instance with the same
    information exists.
    """

    class __MunkiPromoterConfig:
        REPO_PATH = os.getenv(
            "MUNKIPROMOTER_REPO_PATH",
            config_from_file.get(ConfigSections.MUNKI.value, "REPO_PATH"),
        )

        DEBUG_PKGS_INFO_SAVE_PATH = os.getenv(
            "MUNKIPROMOTER_DEBUG_PKGS_INFO_SAVE_PATH",
            config_from_file.get(
                ConfigSections.MUNKI.value, "DEBUG_PKGS_INFO_SAVE_PATH"
            ),
        )
        MAKECATALOGS = os.getenv(
            "MUNKIPROMOTER_MAKECATALOGS",
            config_from_file.get(ConfigSections.MUNKI.value, "MAKECATALOGS"),
        )

        DRY_RUN = os.getenv(
            "MUNKIPROMOTER_DRY_RUN",
            config_from_file.get(ConfigSections.MUNKI.value, "DRY_RUN"),
        )

        MAKECATALOGS_PARAMS = os.getenv(
            "MUNKIPROMOTER_MAKECATALOGS_PARAMS",
            config_from_file.get(
                ConfigSections.MUNKI.value, "MAKECATALOGS_PARAMS"
            ),
        )

        JIRA_URL = os.getenv(
            "MUNKIPROMOTER_JIRA_URL",
            config_from_file.get(ConfigSections.JIRA.value, "JIRA_URL"),
        )
        JIRA_USER = os.getenv(
            "MUNKIPROMOTER_JIRA_USER",
            config_from_file.get(ConfigSections.JIRA.value, "JIRA_USER"),
        )
        JIRA_PASSWORD = os.getenv(
            "MUNKIPROMOTER_JIRA_PASSWORD",
            config_from_file.get(ConfigSections.JIRA.value, "JIRA_PASSWORD"),
        )

        JIRA_PROJECT_KEY = os.getenv(
            "MUNKIPROMOTER_JIRA_PROJECT_KEY",
            config_from_file.get(ConfigSections.JIRA.value, "JIRA_PROJECT_KEY"),
        )
        JIRA_ISSUE_TYPE = os.getenv(
            "MUNKIPROMOTER_JIRA_ISSUE_TYPE",
            config_from_file.get(ConfigSections.JIRA.value, "JIRA_ISSUE_TYPE"),
        )

        JIRA_SOFTWARE_NAME_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_SOFTWARE_NAME_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_SOFTWARE_NAME_FIELD"
            ),
        )
        JIRA_PROJECT_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_PROJECT_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_PROJECT_FIELD"
            ),
        )
        JIRA_ISSUE_TYPE_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_ISSUE_TYPE_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_ISSUE_TYPE_FIELD"
            ),
        )
        JIRA_SUMMARY_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_SUMMARY_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_SUMMARY_FIELD"
            ),
        )
        JIRA_DESCRIPTION_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_DESCRIPTION_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_DESCRIPTION_FIELD"
            ),
        )
        JIRA_SOFTWARE_VERSION_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_SOFTWARE_VERSION_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_SOFTWARE_VERSION_FIELD"
            ),
        )
        JIRA_DUEDATE_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_DUEDATE_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_DUEDATE_FIELD"
            ),
        )
        JIRA_LABELS_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_LABELS_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_LABELS_FIELD"
            ),
        )
        JIRA_CATALOG_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_CATALOG_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_CATALOG_FIELD"
            ),
        )
        JIRA_AUTOPROMOTE_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_AUTOPROMOTE_FIELD"
            ),
        )

        _JIRA_AUTOPROMOTE_TRUE = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_TRUE",
            config_from_file.get(
                ConfigSections.JIRA.value, "_JIRA_AUTOPROMOTE_TRUE"
            ),
        )
        _JIRA_AUTOPROMOTE_FALSE = os.getenv(
            "MUNKIPROMOTER_JIRA_AUTOPROMOTE_FALSE",
            config_from_file.get(
                ConfigSections.JIRA.value, "_JIRA_AUTOPROMOTE_FALSE"
            ),
        )

        JIRA_PRESENT_FIELD = os.getenv(
            "MUNKIPROMOTER_JIRA_PRESENT_FIELD",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_PRESENT_FIELD"
            ),
        )

        JIRA_DEVELOPMENT_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_DEVELOPMENT_TRANSITION_NAME",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_DEVELOPMENT_TRANSITION_NAME"
            ),
        )
        JIRA_TESTING_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_TESTING_TRANSITION_NAME",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_TESTING_TRANSITION_NAME"
            ),
        )
        JIRA_PRODUCTION_TRANSITION_NAME = os.getenv(
            "MUNKIPROMOTER_JIRA_PRODUCTION_TRANSITION_NAME",
            config_from_file.get(
                ConfigSections.JIRA.value, "JIRA_PRODUCTION_TRANSITION_NAME"
            ),
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

        DEFAULT_PROMOTION_INTERVAL = int(
            os.getenv(
                "MUNKIPROMOTER_DEFAULT_PROMOTION_INTERVAL",
                config_from_file.get(
                    ConfigSections.PROMOTION.value, "DEFAULT_PROMOTION_INTERVAL"
                ),
            )
        )
        DEFAULT_PROMOTION_DAY = os.getenv(
            "MUNKIPROMOTER_DEFAULT_PROMOTION_DAY",
            config_from_file.get(
                ConfigSections.PROMOTION.value, "DEFAULT_PROMOTION_DAY"
            ),
        )

        LOG_LEVEL = os.getenv(
            "MUNKIPROMOTER_LOG_LEVEL",
            config_from_file.get(ConfigSections.LOGGER.value, "LOG_LEVEL"),
        )
        LOG_BACKUP_COUNT = os.getenv(
            "MUNKIPROMOTER_LOG_BACKUP_COUNT",
            config_from_file.get(
                ConfigSections.LOGGER.value, "LOG_BACKUP_COUNT"
            ),
        )
        LOG_DIR = os.getenv(
            "MUNKIPROMOTER_LOG_DIR",
            config_from_file.get(ConfigSections.LOGGER.value, "LOG_DIR"),
        )

        LOG_FILENAME = os.getenv(
            "MUNKIPROMOTER_LOG_FILENAME",
            config_from_file.get(ConfigSections.LOGGER.value, "LOG_FILENAME"),
        )

    @property
    def CATALOGS_PATH(self):
        return os.path.join(
            self.instance.REPO_PATH,
            os.getenv(
                "MUNKIPROMOTER_CATALOGS_DIR",
                config_from_file.get(
                    ConfigSections.MUNKI.value, "CATALOGS_DIR"
                ),
            ),
        )

    @property
    def PKGS_INFO_PATH(self):
        return os.path.join(
            self.instance.REPO_PATH,
            os.getenv(
                "MUNKIPROMOTER_PKGS_INFO_DIR",
                config_from_file.get(
                    ConfigSections.MUNKI.value, "PKGS_INFO_DIR"
                ),
            ),
        )

    @property
    def JIRA_CONNECTION_INFO(self):
        # Store Jira connection information in a dict. We can then create a
        # connection by invoking
        # JIRA(**JIRA_CONNECTION_INFO)
        return {
            "server": self.instance.JIRA_URL,
            "basic_auth": (
                self.instance.JIRA_USER,
                self.instance.JIRA_PASSWORD,
            ),
        }

    instance = None

    def __init__(self):
        if not MunkiPromoterConfig.instance:
            MunkiPromoterConfig.instance = (
                MunkiPromoterConfig.__MunkiPromoterConfig()
            )

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        setattr(self.instance, key, value)

    def restore_defaults(self):
        self.__init__()


class MunkiPromoterTestConfig(MunkiPromoterConfig):
    """
    This class has all the same attributes as the MunkiPromoterConfig but
    adds/sets required values for testing.
    """

    def __init__(self):
        super().__init__()
        self.__setattr__(
            "TEST_REPO_PATH",
            os.getenv(
                "MUNKIPROMOTER_TEST_REPO_PATH",
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))
                        )
                    ),
                    "tests/data",
                ),
            ),
        )
        self.instance.REPO_PATH = self.instance.TEST_REPO_PATH
        self.instance.MAKECATALOGS_PARAMS = "--skip-pkg-check"
        self.instance.JIRA_DUMP_PATH = os.path.join(
            os.path.dirname(__file__), "../../tests/jira_dump"
        )
        self.instance.DRY_RUN = True


conf = (
    MunkiPromoterTestConfig()
    if "pytest" in sys.modules
    else MunkiPromoterConfig()
)


class JiraEnum(Enum):
    def to_jira_rest_dict(self):
        """
        When submitting a field to the Jira API it usually requires a dictionary
        with a  key called id and the corresponding value of this id. This
        method simply returns a dict with such key and the value stored in the
        enum instance.
        :return: Dictionary with id key and id value.
        """
        return {"id": self.value}


class JiraLane(JiraEnum):
    """
    This enum models all different lanes available in jira
    """

    TO_DEVELOPMENT = "To Development"
    DEVELOPMENT = "Development"
    TO_TESTING = "To Testing"
    TESTING = "Testing"
    TO_PRODUCTION = "To Production"
    PRODUCTION = "Production"

    @staticmethod
    def catalog_to_lane(catalog: Catalog) -> JiraLane:
        """
        Converts a `Catalog` to a `JiraLane`

        :param catalog: `Catalog` to be converted
        :return: the matching `JiraLane`
        """
        for j_enum in JiraLane:
            if j_enum.name == catalog.name:
                return j_enum

    @property
    def is_promotion_lane(self):
        """
        `Bool` property of the `JiraLane`.

        :return:  True if the `JiraLane` is a promotion lane (TO *catalog*)
        """
        if "TO" in self.name:
            return True
        return False


class Catalog(JiraEnum):
    """
    This enum models the different available catalogs in jira and their jira
    field id.
    """

    DEVELOPMENT = "12007"
    TESTING = "12008"
    PRODUCTION = "12009"

    @staticmethod
    def str_to_catalog(catalog_string: str) -> Catalog:
        """
        Converts a `str` to a `Catalog` if it exists.

        :param catalog_string: `str` the catalog
        :return: `Catalog` the catalog
        """
        catalog_string = (
            catalog_string.upper()
        )  # in case the string is not already all upper case we will do it here
        for c_enum in Catalog:
            if c_enum.name == catalog_string:
                return c_enum

    @staticmethod
    def jira_lane_to_catalog(jira_lane: JiraLane) -> Catalog:
        """
        Convert a `JiraLane` to a `Catalog`

        :param jira_lane: `JiraLane` the jira lane to convert
        :return: `Catalog` the respective catalog
        """
        return Catalog.str_to_catalog(jira_lane.name.replace("TO_", ""))

    @property
    def next_catalog(self) -> Catalog:
        """
        Property of a catalog. The order of the catalogs is DEV -> TEST -> PROD.
        If the next catalog is called for PROD, PROD is returned.

        :return: `Catalog` the subsequent catalog
        """
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
        """
        Property of the Catalog. Returns the transition id as a string.

        :return: id of the given catalog in jira as `str`
        """
        transition_dict = {
            Catalog.DEVELOPMENT: conf.JIRA_DEVELOPMENT_TRANSITION_NAME,
            Catalog.TESTING: conf.JIRA_TESTING_TRANSITION_NAME,
            Catalog.PRODUCTION: conf.JIRA_PRODUCTION_TRANSITION_NAME,
        }

        return transition_dict.get(self)


class Present(JiraEnum):
    """
    This enum models the jira field whether a munki package exists for a jira
    issue.
    """

    PRESENT = "12010"
    MISSING = None


class PackageState(JiraEnum):
    """
    This enum models the package state.
    DEFAULT = No changes
    NEW = New package
    UPDATE = Changes
    """

    DEFAULT = auto()
    NEW = auto()
    UPDATE = auto()


class JiraAutopromote(JiraEnum):
    """
    This enum models if a package will be autopromoted or not. It can be called
    as a bool and will return true if
    the value is PROMOTE.
    """

    PROMOTE = conf._JIRA_AUTOPROMOTE_TRUE
    NOPROMOTE = conf._JIRA_AUTOPROMOTE_FALSE

    def __bool__(self):
        if self.name == self.PROMOTE.name:
            return True
        else:
            return False
