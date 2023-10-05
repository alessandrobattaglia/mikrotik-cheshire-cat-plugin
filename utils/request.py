import requests
from requests.auth import HTTPBasicAuth
from cat.plugins.mikrotik.settings import get_setting


def load_mikrotik_auth(cat):
    return HTTPBasicAuth(
        get_setting(cat, "router_user"),
        get_setting(cat, "router_password")
    )


class Request:
    def __init__(self, base_address, auth=None):
        self.base_address = base_address
        self.auth = auth

    def perform(self, url):
        return requests.get(("" if url.startswith("http") else self.base_address) + url, auth=self.auth, verify=False).json()
