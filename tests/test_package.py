import operator
from datetime import datetime

import pytest
from core import Package, JiraBoardProvider, MunkiRepoProvider
from utils import Catalog, JiraLane, PackageState


@pytest.fixture
def p1(request):
    yield Package(
        "Firefox",
        request.param,
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        False,
        JiraBoardProvider,
        JiraLane.TESTING,
        PackageState.NEW,
    )


@pytest.fixture
def p2(request):
    yield Package(
        "Firefox",
        request.param,
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        False,
        JiraBoardProvider,
        JiraLane.TESTING,
        PackageState.NEW,
    )


def test_package_equality():
    """Identical packages should be equal."""
    p1 = Package(
        "Firefox",
        "61.3.5",
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        False,
        JiraBoardProvider,
        JiraLane.TESTING,
    )

    p2 = Package(
        "Firefox",
        "61.3.5",
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        False,
        JiraBoardProvider,
        JiraLane.TESTING,
    )

    p3 = Package(
        "Firefox",
        "61.3.5",
        Catalog.TESTING,
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
        False,
        False,
        MunkiRepoProvider,
        JiraLane.TESTING,
    )

    assert p1 == p2
    assert p2 != p3
    assert p1 != p3


@pytest.mark.parametrize(
    ["p1", "p2", "op"],
    [("10", "10", operator.eq), ("11", "10", operator.gt), ("10", "11", operator.lt)],
    indirect=["p1", "p2"],
)
def test_package_version_comparision(p1, p2, op):
    """Test the version comparision methods of the package class."""

    assert True == op(p1, p2)
