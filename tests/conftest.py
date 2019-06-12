from datetime import datetime

import pytest
from core.base_classes import Package
from core.providers import JiraBoardProvider, MunkiRepoProvider
from utils.config import Catalog, Present, JiraLane, PackageState, JiraAutopromote


@pytest.fixture
def jira_board_provider():
    return JiraBoardProvider("test_instance")


@pytest.fixture
def munki_repo_provider():
    return MunkiRepoProvider("test_instance")


@pytest.fixture(params=["10"])
def test_one_package(request) -> Package:
    yield Package(
        "Firefox",
        Package.str_to_version(request.param),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        JiraAutopromote.NOPROMOTE,
        Present.PRESENT,
        JiraBoardProvider,
        "SWPM-789",
        JiraLane.TESTING,
        PackageState.NEW,
    )


@pytest.fixture
def test_two_packages(request) -> ["Package"]:
    yield [
        Package(
            "Firefox",
            Package.str_to_version(request.param[0]),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            JiraAutopromote.NOPROMOTE,
            Present.PRESENT,
            JiraBoardProvider,
            "SWPM-7859",
            JiraLane.TESTING,
            PackageState.NEW,
        ),
        Package(
            "Firefox",
            Package.str_to_version(request.param[1]),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            JiraAutopromote.NOPROMOTE,
            Present.PRESENT,
            JiraBoardProvider,
            "SWPM-7859",
            JiraLane.TESTING,
            PackageState.NEW,
        ),
    ]
