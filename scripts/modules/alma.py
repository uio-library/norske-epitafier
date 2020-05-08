from requests import Session
from urllib.parse import urljoin


class AlmaApi:

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.session = Session()
        self.session.headers = {
            'Authorization': 'apikey %s' % api_key,
            'Accept': 'application/json'
        }

    def get(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        return self.session.post(url, **kwargs)
