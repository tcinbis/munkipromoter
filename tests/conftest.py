from datetime import datetime

import pytest
from core.base_classes import Package
from core.providers import JiraBoardProvider
from utils.config import Catalog, Present, JiraLane, PackageState


@pytest.fixture(params=["10"])
def test_one_package(request) -> Package:
    jira_board = JiraBoardProvider(name="_jira")
    yield Package(
        "Firefox",
        Package.str_to_version(request.param),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        Present.PRESENT,
        jira_board,
        "SWPM-789",
        JiraLane.TESTING,
        PackageState.NEW,
    )


@pytest.fixture
def test_two_packages(request) -> ["Package"]:
    jira_board = JiraBoardProvider(name="_jira")
    yield [
        Package(
            "Firefox",
            Package.str_to_version(request.param[0]),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            False,
            Present.PRESENT,
            jira_board,
            "SWPM-7859",
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
            "SWPM-7389",
            JiraLane.TESTING,
            PackageState.NEW,
        ),
    ]
