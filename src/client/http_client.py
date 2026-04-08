import requests
from src.client.base import BaseClient


class HTTPClient(BaseClient):
    
    def get(self, url, params=None):
        return requests.get(url=url, headers=self.headers, params=params)