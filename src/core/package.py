from dataclasses import dataclass, field
from datetime import datetime
from distutils.version import LooseVersion
from typing import Type
from core.providers import Provider
from utils.config import JiraLane, Catalog, PackageState


class PackageVersion(LooseVersion):
    pass


@dataclass(order=True)
class Package:
    name: str = field(repr=True)
    version: LooseVersion = field(repr=True, compare=True)
    catalog: Catalog = field(repr=True, compare=False)
    date: datetime = field(repr=False, compare=False)
    is_autopromote: bool = field(repr=False, compare=False)
    is_present: bool = field(repr=False, compare=False)
    provider: Type[Provider] = field(repr=False, compare=False)
    jira_lane: JiraLane = field(repr=False, compare=False)
    state: PackageState = field(default=PackageState.DEFAULT, repr=False, compare=False)

    @staticmethod
    def str_to_version(version_str: str) -> LooseVersion:
        return LooseVersion(version_str)
