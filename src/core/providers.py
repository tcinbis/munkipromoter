from utils.exceptions import ProviderDoesNotImplement


class Provider:
    def __init__(self, name):
        self.name = name

    def connect(self):
        pass

    def load(self):
        pass

    def get(self):
        pass

    def update(self):
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

    def update(self):
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

    def update(self):
        raise ProviderDoesNotImplement(self.__class__.__name__)
