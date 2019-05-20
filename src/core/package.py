from dataclasses import dataclass, field
from datetime import datetime
from typing import Type
from core.providers import Provider
from utils.config import JiraLane, Catalog, PackageState


@dataclass(order=True)
class Package:
    name: str = field(repr=True)
    version: str = field(repr=True, compare=True)
    catalog: Catalog = field(repr=True)
    date: datetime
    is_autopromote: bool
    is_present: bool
    is_missing: bool
    provider: Type[Provider]
    jira_lane: JiraLane
    state: PackageState

    def __str__(self) -> str:
        return f"Name:{self.name} Version:{self.version}"
