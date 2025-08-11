# client.py

from utils import get_json, memoize
from utils import access_nested_map

def get_json(url):
    """Stub function to be mocked in tests."""
    pass

class GithubOrgClient:
    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        return get_json(f"https://api.github.com/orgs/{self.org_name}")
