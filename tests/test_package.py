import operator
from datetime import datetime

import pytest
from core.base_classes import Package, PackageVersion
from core.providers import JiraBoardProvider
from utils.config import Catalog, JiraLane, PackageState, Present, JiraAutopromote


def test_package_equality():
    """Identical packages should be equal."""
    jira_board = JiraBoardProvider(name="_jira")
    p1 = Package(
        "Firefox",
        Package.str_to_version("61.3.5"),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        JiraAutopromote.NOPROMOTE,
        Present.PRESENT,
        jira_board,
        "SWPM-4556",
        JiraLane.TESTING,
    )

    p2 = Package(
        "Firefox",
        Package.str_to_version("61.3.5"),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        JiraAutopromote.NOPROMOTE,
        Present.PRESENT,
        jira_board,
        "SWPM-4556",
        JiraLane.TESTING,
    )

    assert p1 == p2

    p2.name = "Matlab"

    assert p1 != p2


@pytest.mark.parametrize(
    ["test_two_packages", "op"],
    [
        (("10", "10"), operator.eq),
        (("11", "10"), operator.gt),
        (("10", "11"), operator.lt),
        (("63.21.2a", "63.21.2b"), operator.lt),
        (("123.21.2a", "63.21.2a"), operator.gt),
        (("2019b", "2019a"), operator.gt),
    ],
    indirect=["test_two_packages"],
)
def test_package_version_comparision(test_two_packages, op):
    """Test the version comparision methods of the package class."""

    assert op(test_two_packages[0], test_two_packages[1])


@pytest.mark.parametrize(
    "version", ["10", "11", "63.21.2a", "63.21.2b", "123.21.2a", "2019b", "12.2,3.ä"]
)
def test_str_to_version(version):
    assert isinstance(Package.str_to_version(version), PackageVersion)
