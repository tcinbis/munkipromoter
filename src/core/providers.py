import core
from core.base_classes import Provider, Package
from jira import JIRA
from utils.config import (
    JIRA_PROJECT_FIELD,
    JIRA_PROJECT_KEY,
    JIRA_ISSUE_TYPE,
    JIRA_ISSUE_TYPE_FIELD,
    JIRA_SOFTWARE_NAME_FIELD,
    JIRA_SOFTWARE_VERSION_FIELD,
    JIRA_DUEDATE_FIELD,
    JIRA_DESCRIPTION_FIELD,
    JIRA_LABELS_FIELD,
    JIRA_CATALOG_FIELD,
    JIRA_AUTOPROMOTE_FIELD,
    JIRA_PRESENT_FIELD,
    JIRA_AUTOPROMOTE,
    JIRA_CONNECTION_INFO,
    JIRA_SUMMARY_FIELD,
)
from utils.exceptions import ProviderDoesNotImplement


class MunkiRepoProvider(Provider):
    def __init__(self, name):
        super().__init__(name)

    def connect(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def load(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def get(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def update(self, package: "Package"):
        raise ProviderDoesNotImplement(self.__class__.__name__)


class JiraBoardProvider(Provider):
    def __init__(self, name):
        super().__init__(name)
        # noinspection PyTypeChecker
        self._jira = None  # type: JIRA

    def connect(self):
        self._jira = JIRA(**JIRA_CONNECTION_INFO)

        if self._jira:
            return True
        else:
            return False

    def load(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def get(self):
        query = f"project={JIRA_PROJECT_KEY}"
        search_result = self._jira.search_issues(query, maxResults=500)
        total_issues = search_result.total

        if total_issues != len(search_result):
            # we could only fetch some tickets and need to fetch more
            cumulative_results = list()

            while len(cumulative_results) != total_issues:
                cumulative_results.extend(search_result.iterable)
                start_at = search_result.startAt + len(search_result)
                search_result.clear()
                search_result = self._jira.search_issues(
                    query, startAt=start_at, maxResults=500
                )
            return self._jira_issue_to_package(cumulative_results)

        return self._jira_issue_to_package(search_result)

    def _check_jira_issue_exists(self, package: "Package"):
        pass

    def _jira_issue_to_package(self, issues) -> ["Package"]:
        packages = list()
        for issue in issues:
            packages.append(Package())

        return packages


    def update(self, package: "Package"):
        issue_dict = {
            JIRA_PROJECT_FIELD: JIRA_PROJECT_KEY,
            JIRA_ISSUE_TYPE_FIELD: JIRA_ISSUE_TYPE,
            JIRA_SUMMARY_FIELD: str(package),
            JIRA_SOFTWARE_NAME_FIELD: package.name,
            JIRA_SOFTWARE_VERSION_FIELD: package.version.vstring,
            JIRA_DUEDATE_FIELD: package.date.strftime("%Y-%m-%d"),
            JIRA_DESCRIPTION_FIELD: package.name,
            JIRA_CATALOG_FIELD: [package.catalog.value],
            JIRA_AUTOPROMOTE_FIELD: JIRA_AUTOPROMOTE.get(package.is_autopromote),
            JIRA_PRESENT_FIELD: [package.is_present.value],
        }

        self._jira.create_issue(fields=issue_dict)
