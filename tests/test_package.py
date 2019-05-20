from datetime import datetime

from core import Package, JiraBoardProvider


def test_package_equality():
    """Identical packages should be equal."""
    p1 = Package(
        "Firefox",
        "61.2.3",
        "testing",
        datetime.strptime("10:05:55 01.01.2020","%H:%M:%S %d.%m.%Y"),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    p2 = Package(
        "Firefox",
        "61.2.3",
        "testing",
        datetime.strptime("10:05:55 01.01.2020","%H:%M:%S %d.%m.%Y"),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    assert p1 == p2


def test_package_inequality():
    """Different packages should not be equal."""
    p1 = Package(
        "Firefox",
        "61.2.3",
        "testing",
        datetime.now(),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    p2 = Package(
        "Firefox",
        "61.2.4",
        "testing",
        datetime.now(),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    assert p1 != p2

def test_package_less_than():
    pass