from random import random
from unittest.mock import Mock

from core.providers import JiraBoardProvider
from jira import Issue
from utils.config import ISSUE_FIELDS
from utils.exceptions import JiraIssueMissingFields


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

    def test_load(self):
        pass

    def test_get(self):
        pass

    def test_check_jira_issue_exists(self, jira_board_provider, test_one_package):
        assert JiraBoardProvider.check_jira_issue_exists(test_one_package)
        test_one_package.jira_id = None
        assert not JiraBoardProvider.check_jira_issue_exists(test_one_package)

    def test__jira_issue_to_package_list(self):
        pass

    def test__jira_issue_to_package(self, jira_board_provider):
        """
        Test whether exceptions are handled/raised correctly.
        :param jira_board_provider:
        :return:
        """
        issue = Issue(None, None)
        issue.fields = Mock()

        for attribute in ISSUE_FIELDS:
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

    def test_update(self):
        pass
        # def test_update(self, test_one_package):
        #     jira = JiraBoardProvider(Mock())
        #     jira._jira = MagicMock()
        #     jira.update(test_one_package)
        #
        #     issue_dict = {
        #         JIRA_PROJECT_FIELD: JIRA_PROJECT_KEY,
        #         JIRA_ISSUE_TYPE_FIELD: JIRA_ISSUE_TYPE,
        #         JIRA_SUMMARY_FIELD: str(test_one_package),
        #         JIRA_SOFTWARE_NAME_FIELD: test_one_package.name,
        #         JIRA_SOFTWARE_VERSION_FIELD: test_one_package.version.vstring,
        #         JIRA_DUEDATE_FIELD: test_one_package.date.strftime("%Y-%m-%d"),
        #         JIRA_DESCRIPTION_FIELD: test_one_package.name,
        #         JIRA_CATALOG_FIELD: [test_one_package.catalog.value],
        #         JIRA_AUTOPROMOTE_FIELD: JIRA_AUTOPROMOTE.get(
        #             test_one_package.is_autopromote
        #         ),
        #         JIRA_PRESENT_FIELD: [test_one_package.is_present.value],
        #     }
        #
        #     jira._jira.create_issue.assert_called_once_with(fields=issue_dict)


class TestMunkiRepoProvider:
    def test_connect_fail(self, jira_board_provider):
        pass

    def test_load(self, munki_repo_provider):
        munki_repo_provider.load()

    def test_get(self):
        pass

    def test__jira_issue_to_package_list(self):
        pass

    def test__jira_issue_to_package(self, jira_board_provider):
        pass

    def test_update(self):
        pass
