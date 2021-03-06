#  Gmacht mit ❤️ in Basel
#
#  Copyright (c) 2019 University of Basel
#  Last modified 16/07/2019, 12:55.
#
#  Developed by Tom Cinbis and Tim Königl on 16/07/2019, 13:04


class PromoterException(Exception):
    """This exception class will be extended by all sub exceptions which are
    special to this project."""

    def __init__(self):
        super().__init__()
        self.message = f"{self.__class__} exception occurred."

    def __str__(self):
        return self.message


class ProviderDoesNotImplement(PromoterException):
    """This provider does not implement the given method."""

    def __init__(self, provider="Provider"):
        super().__init__()
        self.provider = provider
        self.message = f"{provider} does not implement the given method."


class JiraIssueMissingFields(PromoterException):
    """This Jira issue does not have all required fields for this method."""

    def __init__(self):
        super().__init__()
        self.provider = "Jira"
        self.message = "Jira issue does not have all required fields."


class MunkiItemInMultipleCatalogs(PromoterException):
    """This munki item is in multiple catalogs at once."""

    def __init__(self, munki_item):
        super().__init__()
        self.provider = "Munki"
        self.munki_item = munki_item
        self.message = (
            f"{munki_item.get('name')} with version "
            f"{munki_item.get('version')} is in more than one catalog. "
            f"Can't process item."
        )


class MunkiRepoNotFound(PromoterException):
    """
    In case we can not find or access the repository we will throw this
    exception
    """

    def __init__(self, repo):
        super().__init__()
        self.provider = "Munki"
        self.message = f"The given Munki repository: {repo} was not found."


class ImproperlyConfigured(PromoterException):
    """
    The ImproperlyConfigured exception is raised when Munki Promoter is somehow
    improperly configured – for example, if a value in config.py is incorrect or
    unparseable.
    """

    def __init__(self):
        super().__init__()
        self.message = "Improper configuration values. See log."
