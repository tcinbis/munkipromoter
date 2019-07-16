from unittest.mock import Mock

from jira.client import ResultList

from core.promotion import Promoter
from tests.conftest import load_jira_test_issue


class TestPromotion:
    def set_up_promoter(self, config, jira_board_provider, munki_repo_provider):
        jira_board_provider._jira = Mock()
        jira_board_provider.is_loaded = True
        jira_issue = [load_jira_test_issue(config.JIRA_DUMP_PATH)]
        result_list = ResultList(jira_issue, _total=len(jira_issue))
        jira_board_provider._jira.search_issues.return_value = result_list
        jira_board_provider.load()

        munki_repo_provider.load()
        munki_repo_provider._packages_dict = {
            k: v
            for k, v in munki_repo_provider._packages_dict.items()
            if "EN60.8.0" in k
        }

        return Promoter(
            munki_repo_provider._packages_dict, jira_board_provider._packages_dict
        )