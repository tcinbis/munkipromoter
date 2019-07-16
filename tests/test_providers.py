#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04

import copy
from datetime import datetime
from random import random
from unittest.mock import Mock

import pytest
from jira import Issue
from jira.client import ResultList

from core.base_classes import Package
from core.provider.jiraprovider import JiraBoardProvider
from core.provider.munkiprovider import MunkiRepoProvider
from utils.config import PackageState, Present
from utils.exceptions import JiraIssueMissingFields


@pytest.mark.usefixtures("run_makecatalogs_before")
class TestJiraBoardProvider:
    def test_connect_fail(self, jira_board_provider):
        # These parameters are supposed to fail to test, whether exceptions are handled correctly.
        param = {
            "server": "http://your-jira.com",
            "basic_auth": ("your-user", "secret_passw0rd123"),
            "max_retries": 0,
        }

        # When a connection is not possible the method should return False and do not throw a exception.
        assert not jira_board_provider.connect(connection_params=param)

    def test_load(self, jira_board_provider, jira_test_issues):
        jira_board_provider._jira = Mock()
        jira_board_provider.is_loaded = True
        jira_issue = [jira_test_issues]
        result_list = ResultList(jira_issue, _total=len(jira_issue))
        jira_board_provider._jira.search_issues.return_value = result_list
        jira_board_provider.load()

        assert len(jira_board_provider.get()) != 0

    def test_check_jira_issue_exists(self, jira_board_provider, test_one_package):
        assert JiraBoardProvider.check_jira_issue_exists(test_one_package)
        test_one_package.jira_id = None
        assert not JiraBoardProvider.check_jira_issue_exists(test_one_package)

    def test__jira_issue_to_package_list(self, jira_board_provider):
        issue_mock = Mock()
        issue_mock.fields = None

        with pytest.raises(AttributeError):
            jira_board_provider._jira_issue_to_package(issue_mock)

    def test__jira_issue_to_package(self, jira_board_provider, config):
        """
        Test whether exceptions are handled/raised correctly.
        :param jira_board_provider:
        :return:
        """
        issue = Issue(None, None)
        issue.fields = Mock()

        for attribute in config.ISSUE_FIELDS:
            issue.fields.__setattr__(attribute, str(random()))

        try:
            jira_board_provider._jira_issue_to_package(issue)
        except AttributeError:
            assert True

        issue.fields = object

        try:
            jira_board_provider._jira_issue_to_package(issue)
        except JiraIssueMissingFields:
            assert True

    def test_update(self, jira_board_provider, jira_test_issues):

        jira_board_provider._jira = Mock()
        jira_board_provider.is_loaded = True
        jira_issue = [jira_test_issues]
        result_list = ResultList(jira_issue, _total=len(jira_issue))
        jira_board_provider._jira.search_issues.return_value = result_list
        jira_board_provider.load()

        packages = copy.deepcopy(jira_board_provider.get())

        # after loading our testing repo, we should have more than 0 packages
        assert len(packages) != 0

        test_key = list(packages.keys())[0]
        p = packages.get(test_key)  # type: Package
        p.catalog = None
        jira_board_provider.update(p)

        for key, package in jira_board_provider.get().items():
            # after changing the value of a not ignored package field the update should be propagated and be represented
            # in the new dictionary we get from our munki provider
            assert packages.get(key).is_exact_match(package, ["state"])

    def test_update_new_package(
        self, jira_board_provider, jira_test_issues, random_package
    ):
        jira_board_provider._jira = Mock()
        jira_board_provider.is_loaded = True
        jira_issue = [jira_test_issues]
        result_list = ResultList(jira_issue, _total=len(jira_issue))
        jira_board_provider._jira.search_issues.return_value = result_list
        jira_board_provider.load()

        jira_packages = copy.deepcopy(jira_board_provider.get())

        # because we want to simulate a new package it can not have a jira id already
        random_package.jira_id = None
        jira_board_provider.update(random_package)

        jira_package = jira_board_provider._get(random_package.key)

        assert (
            random_package.key in jira_board_provider.get()
            and random_package.key not in jira_packages
        )
        assert random_package.is_exact_match(jira_package, ["state"])
        assert jira_package.state == PackageState.NEW

    def test_update_jira_from_repo(self, munki_repo_provider, jira_board_provider):
        munki_repo_provider.load()
        munki_packages = copy.deepcopy(munki_repo_provider.get())

        jira_board_provider._jira = Mock()
        jira_board_provider.is_loaded = True
        jira_issue = []
        result_list = ResultList(jira_issue, _total=len(jira_issue))
        jira_board_provider._jira.search_issues.return_value = result_list
        jira_board_provider.load()

        assert len(munki_repo_provider.get()) != 0
        assert len(jira_board_provider.get()) == 0

        jira_board_provider.update_jira_from_repo(munki_packages)

        assert len(jira_board_provider.get()) != 0


@pytest.mark.usefixtures("run_makecatalogs_before")
class TestMunkiRepoProvider:
    def test_connect_fail(self, munki_repo_provider, config):
        config.REPO_PATH = "/some/directory/which/does/not/exist"
        assert not munki_repo_provider.connect()
        config.restore_defaults()
        assert munki_repo_provider.connect()

    def test_load(self, munki_repo_provider):
        munki_repo_provider.load()
        assert len(munki_repo_provider.get()) != 0

    def test_get(self):
        pass

    def test_update_existing_package(self, munki_repo_provider):
        munki_repo_provider.load()
        packages = copy.deepcopy(munki_repo_provider.get())

        # after loading our testing repo, we should have more than 0 packages
        assert len(packages) != 0

        test_key = list(packages.keys())[0]
        p = packages.get(test_key)  # type: Package
        p.catalog = None
        munki_repo_provider.update(p)

        for key, package in munki_repo_provider.get().items():
            # after changing the value of a not ignored package field the update should be propagated and be represented
            # in the new dictionary we get from our munki provider
            assert packages.get(key).is_exact_match(package, ["state"])

        munki_repo_provider.load()
        packages = copy.deepcopy(munki_repo_provider.get())
        p = packages.get(test_key)  # type: Package
        p.promote_date = datetime.now()
        munki_repo_provider.update(p)

        munki_package = munki_repo_provider.get().get(test_key)  # type: Package

        assert not p.is_exact_match(munki_package)

    def test_update_missing_package(self, munki_repo_provider, random_package):
        munki_repo_provider.load()

        munki_repo_provider.update(random_package)
        munki_package = munki_repo_provider._get(random_package.key)

        # when inserting/updating a package which is not present in the munki repo the following attributes need
        # to be set for the package which is passed to the update method AND the package which is actually inserted
        # into the internal dictionary containing all the packages.
        assert (
            random_package.state is PackageState.UPDATE
            and random_package.is_present is Present.MISSING
            and munki_package.state is PackageState.NEW
        )

    def test_make_catalogs_subprocess_error(self, config):
        config.REPO_PATH = "/some/path/which/does/not/exist"
        MunkiRepoProvider.make_catalogs()
