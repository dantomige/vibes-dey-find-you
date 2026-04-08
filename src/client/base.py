from abc import abstractmethod

class BaseClient:

    def __init__(self, headers):
        self.header = headers

    @abstractmethod
    def get(self, endpoint):
        pass