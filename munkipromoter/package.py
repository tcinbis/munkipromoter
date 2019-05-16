class Package:
    def __init__(
        self,
        name,
        version,
        catalog,
        date,
        is_autopromote,
        is_present,
        is_missing,
        provider,
        jira_lane,
        state,
    ):
        self.name = name
        self.version = version
        self.catalog = catalog
        self.date = date
        self.is_autopromote = is_autopromote
        self.is_present = is_present
        self.is_missing = is_missing
        self.provider = provider
        self.jira_lane = jira_lane
        self.state = state

    def __lt__(self, other):
        """
        Less than x < y
        Compare to objects with respect to their version?
        """
        pass

    def __le__(self, other):
        """
        Less equal x <= y
        Compare to objects with respect to their version?
        """
        pass

    def __eq__(self, other):
        """
        Equal x == y
        Considers all instance fields and compares its values.
        """
        for field in filter(lambda a: not a.startswith("__"), dir(self)):
            if not (self.__getattribute__(field) == other.__getattribute__(field)):
                return False
        return True

    def __ne__(self, other):
        """Not equal x != y"""
        return not self.__eq__(other)

    def __gt__(self, other):
        """
        Greater than x >= y
        Compare to objects with respect to their version?
        """
        pass

    def __ge__(self, other):
        """
        Greater equal x > y
        Compare to objects with respect to their version?
        """
        pass

    def __str__(self):
        return f"Name:{self.name} Version:{self.version}"
