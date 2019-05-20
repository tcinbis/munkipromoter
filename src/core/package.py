from dataclasses import dataclass, field
from datetime import datetime
from typing import Type
from core.providers import Provider


@dataclass(order=True)
class Package:
    name: str = field(repr=True)
    version: str = field(repr=True, compare=True)
    catalog: str = field(repr=True)
    date: datetime
    is_autopromote: bool
    is_present: bool
    is_missing: bool
    provider: Type[Provider]
    jira_lane: str
    state: str

    def __str__(self) -> str:
        return f"Name:{self.name} Version:{self.version}"
