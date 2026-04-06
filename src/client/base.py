from abc import abstractmethod

class BaseClient:

    @abstractmethod
    def get(self, endpoint, headers=None):
        pass