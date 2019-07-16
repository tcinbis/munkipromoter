#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 13:02.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import json
import os
import random
import string
from datetime import datetime
from unittest.mock import Mock

import pytest
from jira.client import ResultList
from jira.resources import cls_for_resource

from core.base_classes import Package
from core.promotion import Promoter
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from munkipromoter import MunkiPromoter
from utils.config import Catalog, Present, JiraLane, PackageState, JiraAutopromote, conf


def load_jira_test_issue(jira_dump_path):
    with open(os.path.join(jira_dump_path, "firefox_jira_issue.txt"), "r") as infile:
        dump = json.load(infile)
        return cls_for_resource(dump["self"])(None, None, dump)


@pytest.fixture
def config():
    conf.restore_defaults()
    return conf


@pytest.fixture
def jira_board_provider():
    return JiraBoardProvider("test_instance")


@pytest.fixture
def munki_repo_provider():
    return MunkiRepoProvider("test_instance")


@pytest.fixture
def run_makecatalogs_before(munki_repo_provider):
    munki_repo_provider.make_catalogs()


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


def get_random_string(string_length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))


@pytest.fixture
def random_package() -> Package:
    yield Package(
        name=get_random_string(10),
        version=Package.str_to_version(str(random.uniform(0, 100))),
        catalog=Catalog(random.choices([e.value for e in Catalog])[0]),
        promote_date=datetime.now(),
        is_autopromote=JiraAutopromote(
            random.choices([e.value for e in JiraAutopromote])[0]
        ),
        is_present=Present(random.choices([e.value for e in Present])[0]),
        provider=JiraBoardProvider,
        jira_id=get_random_string(9),
        jira_lane=JiraLane(random.choices([e.value for e in JiraLane])[0]),
        state=PackageState(random.choices([e.value for e in PackageState])[0]),
    )


@pytest.fixture
def set_up_promoter(config, jira_board_provider, munki_repo_provider):
    jira_board_provider._jira = Mock()
    jira_board_provider.is_loaded = True
    jira_issue = [load_jira_test_issue(config.JIRA_DUMP_PATH)]
    result_list = ResultList(jira_issue, _total=len(jira_issue))
    jira_board_provider._jira.search_issues.return_value = result_list
    jira_board_provider.load()

    munki_repo_provider.load()
    munki_repo_provider._packages_dict = {
        k: v for k, v in munki_repo_provider._packages_dict.items() if "EN60.8.0" in k
    }

    return Promoter(
        munki_repo_provider._packages_dict, jira_board_provider._packages_dict
    )
