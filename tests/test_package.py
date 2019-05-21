import operator
from datetime import datetime

import pytest
from core.package import Package
from core.providers import JiraBoardProvider
from utils.config import Catalog, JiraLane, PackageState, Present


@pytest.fixture
def p1(request):
    jira_board = JiraBoardProvider(name="jira")
    yield Package(
        "Firefox",
        request.param,
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        Present.PRESENT,
        jira_board,
        JiraLane.TESTING,
        PackageState.NEW,
    )


@pytest.fixture
def p2(request):
    jira_board = JiraBoardProvider(name="jira")
    yield Package(
        "Firefox",
        Package.str_to_version(request.param),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        Present.PRESENT,
        jira_board,
        JiraLane.TESTING,
        PackageState.NEW,
    )


def test_package_equality():
    """Identical packages should be equal."""
    jira_board = JiraBoardProvider(name="jira")
    p1 = Package(
        "Firefox",
        Package.str_to_version("61.3.5"),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        Present.PRESENT,
        jira_board,
        JiraLane.TESTING,
    )

    p2 = Package(
        "Firefox",
        Package.str_to_version("61.3.5"),
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        Present.PRESENT,
        jira_board,
        JiraLane.TESTING,
    )

    assert p1 == p2

    p2.name = "Matlab"

    assert p1 != p2



@pytest.mark.parametrize(
    ["p1", "p2", "op"],
    [
        ("10", "10", operator.eq),
        ("11", "10", operator.gt),
        ("10", "11", operator.lt),
        ("63.21.2a", "63.21.2b", operator.lt),
        ("123.21.2a", "63.21.2a", operator.gt),
        ("2019b", "2019a", operator.gt),
    ],
    indirect=["p1", "p2"],
)
def test_package_version_comparision(p1, p2, op):
    """Test the version comparision methods of the package class."""

    assert op(p1, p2)
