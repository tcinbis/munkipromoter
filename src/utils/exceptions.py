class ProviderDoesNotImplement(Exception):
    """This provider does not implement the given method."""

    def __init__(self, provider="Provider"):
        super().__init__()
        self.provider = provider
        self.message = f"{provider} does not implement the given method."

    def __str__(self):
        return self.message


class JiraIssueMissingFields(Exception):
    """This Jira issue does not have all required fields for this method."""

    def __init__(self):
        super().__init__()
        self.provider = "Jira"
        self.message = "Jira issue does not have all required fields."

    def __str__(self):
        return self.message
