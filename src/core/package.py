from dataclasses import dataclass, field
from datetime import datetime
from typing import Type
from core.providers import Provider
from utils.config import JiraLane, Catalog, PackageState


@dataclass(order=True)
class Package:
    name: str = field(repr=True)
    version: str = field(repr=True, compare=True)
    catalog: Catalog = field(repr=True, compare=False)
    date: datetime = field(repr=False, compare=False)
    is_autopromote: bool = field(repr=False, compare=False)
    is_present: bool = field(repr=False, compare=False)
    provider: Type[Provider] = field(repr=False, compare=True)
    jira_lane: JiraLane = field(repr=False, compare=True)
    state: PackageState = field(default=PackageState.DEFAULT, repr=False, compare=False)
