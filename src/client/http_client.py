import requests
from src.client.base import BaseClient


class HTTPClient(BaseClient):
    
    def get(self, url):
        return requests.get(url=url, headers=self.headers)