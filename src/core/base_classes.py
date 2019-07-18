#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 15:23.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 15:23

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from distutils.version import LooseVersion
from typing import Type, Dict
from uuid import UUID

from utils import logger as log
from utils.config import PackageState, Catalog, JiraAutopromote, Present, JiraLane, conf

logger = log.get_logger(__file__)


class Provider:
    """
    Abstract interface to model a package information provider.
    """

    def __init__(self, name: str, dry_run: bool = conf.DRY_RUN):
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
        """
        Loads the information or packages of the provider implementation
        """
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
        """
        Gets a package based on the package key.
        :param package_key: unique identifier for the package
        :return: `Package` the package that was searched
        """
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
    """
    The general representation of package information. Either jira issues or munki packages can be represented.
    """
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
        """
        Converts a version `str` into a `PackageVersion`
        :param version_str: the version as `str`
        :return: the version as `PackageVersion`
        """
        return PackageVersion(version_str)

    def __str__(self):
        """
        The string representation of a `Package`
        :return: the name, version and catalog of the package
        """
        return f"{self.name} {self.version} {self.catalog.name}"

    @property
    def key(self):
        """
        The unique identifier of a package consisting of the name and the version
        :return: `str` with name and version
        """
        return self.name + str(self.version)

    @staticmethod
    def ignored_compare_keys():
        """
        :return: List of keys which should be ignored when comparing packages
        """
        return ["promote_date", "jira_id", "munki_uuid", "provider", "state"]
