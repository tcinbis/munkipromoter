from core.base_classes import Provider, Package
from jira import JIRA, Issue
from utils.config import (
    JIRA_PROJECT_FIELD,
    JIRA_PROJECT_KEY,
    JIRA_ISSUE_TYPE,
    JIRA_ISSUE_TYPE_FIELD,
    JIRA_SOFTWARE_NAME_FIELD,
    JIRA_SOFTWARE_VERSION_FIELD,
    JIRA_DUEDATE_FIELD,
    JIRA_DESCRIPTION_FIELD,
    JIRA_CATALOG_FIELD,
    JIRA_AUTOPROMOTE_FIELD,
    JIRA_PRESENT_FIELD,
    JIRA_AUTOPROMOTE,
    JIRA_CONNECTION_INFO,
    JIRA_SUMMARY_FIELD,
    ISSUE_FIELDS,
    PackageState,
    JiraLane,
    Catalog,
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

    def _jira_issue_to_package(self, issues: [Issue]) -> ["Package"]:
        packages = list()
        for issue in issues:
            fields_dict = issue.fields.__dict__  # type: dict

            if all(field in fields_dict for field in ISSUE_FIELDS):
                # Before we try to get all fields from our issue we check, whether all fields are present as keys
                p = Package(
                    name=fields_dict.get(JIRA_SOFTWARE_NAME_FIELD),
                    version=fields_dict.get(JIRA_SOFTWARE_VERSION_FIELD),
                    # TODO: Remove index 0 as catalog field will be changed to RadioSelect
                    catalog=Catalog(fields_dict.get(JIRA_CATALOG_FIELD)[0].id),
                    date=fields_dict.get(JIRA_DUEDATE_FIELD),
                    is_autopromote=fields_dict.get(JIRA_AUTOPROMOTE_FIELD),
                    is_present=fields_dict.get(JIRA_PRESENT_FIELD),
                    provider=self,
                    jira_id=fields_dict.get("key"),
                    jira_lane=JiraLane(fields_dict.get("status").name),
                    state=PackageState.DEFAULT,
                )

                packages.append(p)

        return packages

    def update(self, package: "Package"):
        issue_dict = {
            # TODO: Add/Set status
            # TODO: Add/Set Package State
            JIRA_PROJECT_FIELD: JIRA_PROJECT_KEY,
            JIRA_ISSUE_TYPE_FIELD: JIRA_ISSUE_TYPE,
            JIRA_SUMMARY_FIELD: str(package),
            JIRA_SOFTWARE_NAME_FIELD: package.name,
            JIRA_SOFTWARE_VERSION_FIELD: package.version.vstring,
            JIRA_DUEDATE_FIELD: package.date.strftime("%Y-%m-%d"),
            JIRA_DESCRIPTION_FIELD: package.name,
            JIRA_CATALOG_FIELD: [package.catalog.to_jira_rest_dict()],
            JIRA_AUTOPROMOTE_FIELD: JIRA_AUTOPROMOTE.get(package.is_autopromote),
            JIRA_PRESENT_FIELD: [package.is_present.to_jira_rest_dict()],
        }

        self._jira.create_issue(fields=issue_dict)
