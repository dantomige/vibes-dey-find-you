import requests
from src.client.base import BaseClient


class HTTPClient(BaseClient):
    
    def get(self, endpoint, header=None):
        raise NotImplementedError