import core.package
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
    JIRA_SUMMARY_FIELD)
from utils.exceptions import ProviderDoesNotImplement


class Provider:
    def __init__(self, name):
        self.name = name

    def connect(self) -> bool:
        """
        Check whether a connection is already established or try to establish a new one.
        :return: True if the connection was already established or a new one could be created. Otherwise False
        """
        pass

    def load(self):
        pass

    def get(self):
        pass

    def update(self, package: 'core.package.Package'):
        """
        Updates the information of a package if it already exists or will create a new package.
        All parameters are expected to be passed through **kwargs.
        :return: True if successful or False if not.
        """
        pass


class MunkiRepoProvider(Provider):
    def __init__(self, name):
        super().__init__(name)

    def connect(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def load(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def get(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def update(self, package: 'core.package.Package'):
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
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def update(self, package: 'core.package.Package'):
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
