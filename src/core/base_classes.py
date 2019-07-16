from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from distutils.version import LooseVersion
from typing import Type, Dict, List
from uuid import UUID

from utils import logger as log
from utils.config import PackageState, Catalog, JiraAutopromote, Present, JiraLane

logger = log.get_logger(__file__)


class Provider:
    def __init__(self, name: str, dry_run: bool = False):
        self.name = name
        self.is_loaded = False
        self._packages = list()
        self._packages_dict = dict()
        self._dry_run = dry_run

    def connect(self) -> bool:
        """
        Check whether a connection is already established or try to establish a new one.
        :return: True if the connection was already established or a new one could be created. Otherwise False
        """
        pass

    def load(self) -> None:
        pass

    def get(self) -> Dict:
        """
        If the providers load method was already called this method will return all received packages in a dict.
        Otherwise it will first call load and then return the results.
        :return: dict of Packages offered/received from the providers source.
        """
        if not self.is_loaded:
            logger.debug("Provider not yet loaded. Loading now...")
            self.load()
            logger.debug("Loading complete.")
        return self._packages_dict

    def _get(self, package_key: str) -> Package:
        return self.get().get(package_key)

    def update(self, package: Package):
        """
        Updates the information of a package if it already exists or will create a new package.
        All parameters are expected to be passed through **kwargs.
        :return: True if successful or False if not.
        """
        pass

    def commit(self) -> bool:
        """
        This method finally commits all changes to the providers API in case _dry_run is set to false.
        Otherwise no changes will be send to the provider.
        :return: True in case the changes were committed otherwise False
        """
        pass


class PackageVersion(LooseVersion):
    pass


@dataclass(order=True)
class Package:
    name: str = field(repr=True, compare=True)
    version: PackageVersion = field(repr=True, compare=True)
    catalog: Catalog = field(repr=True, compare=True)
    promote_date: datetime = field(repr=False, compare=False)
    is_autopromote: JiraAutopromote = field(repr=False, compare=False)
    is_present: Present = field(repr=False, compare=True)
    provider: Type[Provider] = field(repr=False, compare=False)
    jira_id: str = field(repr=False, compare=False)
    jira_lane: JiraLane = field(repr=False, compare=True)
    state: PackageState = field(default=PackageState.DEFAULT, repr=False, compare=False)
    munki_uuid: UUID = field(repr=False, default=None, compare=False)

    @staticmethod
    def str_to_version(version_str: str) -> PackageVersion:
        return PackageVersion(version_str)

    def __str__(self):
        return f"{self.name} {self.version} {self.catalog.name}"

    @property
    def key(self):
        return self.name + str(self.version)

    @staticmethod
    def ignored_compare_keys():
        """
        :return: List of keys which should be ignored when comparing packages
        """
        return ["promote_date", "jira_id", "munki_uuid", "provider", "state"]

    def is_exact_match(self, package: Package, exclude_keys: List = None) -> bool:
        """
        Compare ALL fields of a package to another package to check whether we have found an exact match.
        :param package: The package we want to compare us to.
        :param exclude_keys: Ignore the following keys during comparison
        :return: True if all values are the same, False otherwise
        """
        for key, value in package.__dict__.items():
            if (exclude_keys and key not in exclude_keys) or not exclude_keys:
                # only check if the key is in exclude_keys if we are sure that it is not None. In case it is None we
                # want to compare all keys anyways.
                if self.__dict__.get(key) != value:
                    return False
        return True
