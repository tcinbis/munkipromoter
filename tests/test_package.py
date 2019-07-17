#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import copy
import operator
from datetime import datetime, timedelta

import pytest

from core.base_classes import Package, PackageVersion
from core.provider.jiraprovider import JiraBoardProvider
from utils.config import Catalog, JiraLane, Present, JiraAutopromote


class TestPackage:
    def test_ignored_compare_keys(self):
        assert [
            "promote_date",
            "jira_id",
            "munki_uuid",
            "provider",
            "state",
        ] == Package.ignored_compare_keys()

    def test_is_exact_match(self, random_package):
        assert random_package.is_exact_match(random_package)
        p = copy.deepcopy(random_package)
        p.promote_date = datetime.now() + timedelta(days=5)
        assert not random_package.is_exact_match(p)

    def test_package_equality(self):
        """Identical packages should be equal."""
        p1 = Package(
            "Firefox",
            Package.str_to_version("61.3.5"),
            Catalog.TESTING,
            datetime.strptime("10:05:55 01.01.2020", "%H:%M:%S %d.%m.%Y"),
            JiraAutopromote.NOPROMOTE,
            Present.PRESENT,
            JiraBoardProvider,
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
            JiraBoardProvider,
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
    def test_package_version_comparision(self, test_two_packages, op):
        """Test the version comparision methods of the package class."""

        assert op(test_two_packages[0], test_two_packages[1])

    @pytest.mark.parametrize(
        "version",
        ["10", "11", "63.21.2a", "63.21.2b", "123.21.2a", "2019b", "12.2,3.ä"],
    )
    def test_str_to_version(self, version):
        assert isinstance(Package.str_to_version(version), PackageVersion)
