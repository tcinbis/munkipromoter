from datetime import datetime

import pytest
from core.package import Package
from core.providers import JiraBoardProvider
from utils.config import Catalog, Present, JiraLane, PackageState


@pytest.fixture
def test_two_packages(request) -> [Package]:
    jira_board = JiraBoardProvider(name="jira")
    yield [
        Package(
            "Firefox",
            Package.str_to_version(request.param[0]),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            False,
            Present.PRESENT,
            jira_board,
            JiraLane.TESTING,
            PackageState.NEW,
        ),
        Package(
            "Firefox",
            Package.str_to_version(request.param[1]),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            False,
            Present.PRESENT,
            jira_board,
            JiraLane.TESTING,
            PackageState.NEW,
        ),
    ]
