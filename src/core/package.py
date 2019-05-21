from dataclasses import dataclass, field
from datetime import datetime
from distutils.version import LooseVersion

from core.providers import Provider
from utils.config import JiraLane, Catalog, PackageState, Present


class PackageVersion(LooseVersion):
    pass


@dataclass(order=True)
class Package:
    name: str = field(repr=True)
    version: LooseVersion = field(repr=True, compare=True)
    catalog: Catalog = field(repr=True, compare=False)
    date: datetime = field(repr=False, compare=False)
    is_autopromote: bool = field(repr=False, compare=False)
    is_present: Present = field(repr=False, compare=False)
    provider: Provider = field(repr=False, compare=False)
    jira_lane: JiraLane = field(repr=False, compare=False)
    state: PackageState = field(default=PackageState.DEFAULT, repr=False, compare=False)

    @staticmethod
    def str_to_version(version_str: str) -> LooseVersion:
        return LooseVersion(version_str)

    def update(self):
        """
        Call the update method of the provider which created the package.
        :param kwargs: all fields which are defined in the package shall be passed on as a dict
        :return: None
        """
        self.provider.update(self)
