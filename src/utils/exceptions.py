class PromoterException(Exception):
    """This exception class will be extended by all sub exceptions which are special to this project."""

    def __init__(self):
        super().__init__()
        self.message = f"{self.__class__} exception occurred."


class ProviderDoesNotImplement(PromoterException):
    """This provider does not implement the given method."""

    def __init__(self, provider="Provider"):
        super().__init__()
        self.provider = provider
        self.message = f"{provider} does not implement the given method."

    def __str__(self):
        return self.message


class JiraIssueMissingFields(PromoterException):
    """This Jira issue does not have all required fields for this method."""

    def __init__(self):
        super().__init__()
        self.provider = "Jira"
        self.message = "Jira issue does not have all required fields."

    def __str__(self):
        return self.message


class MunkiItemInMultipleCatalogs(PromoterException):
    def __init__(self, munki_item):
        super().__init__()
        self.provider = "Munki"
        self.munki_item = munki_item
        self.message = f"{munki_item.name} in version {munki_item.version} is in more than one catalog. Can't process item. "
