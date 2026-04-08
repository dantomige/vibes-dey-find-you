from abc import abstractmethod

class BaseClient:

    def __init__(self, headers):
        self.headers = headers

    @abstractmethod
    def get(self, endpoint):
        pass