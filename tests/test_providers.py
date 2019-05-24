from unittest.mock import MagicMock, Mock

from core.providers import JiraBoardProvider
from utils.config import *


class TestJiraBoardProvider(object):
    def setUp(self):
        self.jiraBoardProvider = MagicMock()

    def test_connect(self):
        pass

    def test_load(self):
        pass

    def test_get(self):
        pass

    def test_update(self, test_one_package):
        jira = JiraBoardProvider(Mock())
        jira._jira = MagicMock()
        jira.update(test_one_package)

        issue_dict = {
            JIRA_PROJECT_FIELD: JIRA_PROJECT_KEY,
            JIRA_ISSUE_TYPE_FIELD: JIRA_ISSUE_TYPE,
            JIRA_SOFTWARE_NAME_FIELD: test_one_package.name,
            JIRA_SOFTWARE_VERSION_FIELD: test_one_package.version,
            JIRA_DUEDATE_FIELD: test_one_package.date,
            JIRA_DESCRIPTION_FIELD: test_one_package,
            JIRA_LABELS_FIELD: test_one_package.state,
            JIRA_CATALOG_FIELD: test_one_package.catalog,
            JIRA_AUTOPROMOTE_FIELD: JIRA_AUTOPROMOTE.get(test_one_package.is_autopromote),
            JIRA_PRESENT_FIELD: test_one_package.is_present,
        }

        jira._jira.create_issue.assert_called_once_with(fields=issue_dict)
