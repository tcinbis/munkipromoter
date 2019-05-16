class ProviderDoesNotImplement(Exception):
    """This provider does not implement the given method."""

    def __init__(self, provider="Provider"):
        super().__init__()
        self.provider = provider
        self.message = f"{provider} does not implement the given method."

    def __str__(self):
        return self.message
