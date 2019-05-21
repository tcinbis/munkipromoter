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

    def update(self, **kwargs):
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

    def update(self, **kwargs):
        raise ProviderDoesNotImplement(self.__class__.__name__)


class JiraBoardProvider(Provider):
    def __init__(self, name):
        super().__init__(name)

    def connect(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def load(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def get(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)

    def update(self, **kwargs):
        raise ProviderDoesNotImplement(self.__class__.__name__)
