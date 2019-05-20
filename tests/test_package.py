from datetime import datetime

from core import Package, JiraBoardProvider


def test_package_equality():
    """Identical packages should be equal."""
    p1 = Package(
        "Firefox",
        "61.2.3",
        "testing",
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
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
        datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
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


def test_package_version_comparision():
    """Test the version comparision methods of the package class."""
    p1 = Package(
        "Firefox",
        "61.2.1",
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

    p3 = Package(
        "Firefox",
        "61.2.1a",
        "testing",
        datetime.now(),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    p4 = Package(
        "Firefox",
        "61.3.1a",
        "testing",
        datetime.now(),
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    assert p1 < p2
    assert p1 < p3
    assert p3 < p2
    assert p1 == p1
    assert p3 > p1
    assert p3 >= p1
    assert p4 > p1
    assert p4 > p2
    assert p4 > p3
    assert p4 >= p4
