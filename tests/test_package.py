from core import Package, JiraBoardProvider


def test_package_equality():
    """Identical packages should be equal."""
    p1 = Package(
        "Firefox",
        "61.2.3",
        "testing",
        "23.02.2019",
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
        "23.02.2019",
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
        "23.02.2019",
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
        "23.02.2019",
        False,
        False,
        False,
        JiraBoardProvider,
        "testing",
        "present",
    )

    assert p1 != p2
