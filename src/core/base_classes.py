from dataclasses import dataclass, field
from datetime import datetime
from distutils.version import LooseVersion
import utils.config
from utils.config import PackageState
from utils import logger as l

logger = l.get_logger(__file__)


class Provider:
    def __init__(self, name):
        self.name = name
        self.is_loaded = False
        self._packages = list()

    def connect(self) -> "bool":
        """
        Check whether a connection is already established or try to establish a new one.
        :return: True if the connection was already established or a new one could be created. Otherwise False
        """
        pass

    def load(self) -> "None":
        pass

    def get(self) -> "[Package]":
        """
        If the providers load method was already called this method will return all received packages in a list.
        Otherwise it will first call load and then return the results.
        :return: list of Packages offered/received from the providers source.
        """
        if not self.is_loaded:
            logger.debug("Provider not yet loaded. Loading now...")
            self.load()
        logger.debug("Loading complete.")

    def update(self, package: "Package"):
        """
        Updates the information of a package if it already exists or will create a new package.
        All parameters are expected to be passed through **kwargs.
        :return: True if successful or False if not.
        """
        pass


class PackageVersion(LooseVersion):
    pass


@dataclass(order=True)
class Package:
    name: "str" = field(repr=True)
    version: "PackageVersion" = field(repr=True, compare=True)
    catalog: "utils.config.Catalog" = field(repr=True, compare=False)
    date: "datetime" = field(repr=False, compare=False)
    is_autopromote: "utils.config.JiraAutopromote" = field(repr=False, compare=False)
    is_present: "utils.config.Present" = field(repr=False, compare=False)
    provider: "Provider" = field(repr=False, compare=False)
    jira_id: "str" = field(repr=False, compare=False)
    jira_lane: "utils.config.JiraLane" = field(repr=False, compare=False)
    state: "utils.config.PackageState" = field(
        default=PackageState.DEFAULT, repr=False, compare=False
    )

    @staticmethod
    def str_to_version(version_str: "str") -> "PackageVersion":
        return PackageVersion(version_str)

    def update(self):
        """
        Call the update method of the provider which created the package.
        :param kwargs: all fields which are defined in the package shall be passed on as a dict
        :return: None
        """
        self.provider.update(self)

    def __str__(self):
        return f"{self.name} {self.version} {self.catalog.name}"
