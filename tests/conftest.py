import json
import os
import random
import string
from datetime import datetime

import pytest
from core.base_classes import Package
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from jira.resources import cls_for_resource
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
