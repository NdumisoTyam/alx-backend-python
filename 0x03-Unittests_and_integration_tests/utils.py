# utils.py

import requests
from functools import wraps

def get_json(url):
    response = requests.get(url)
    return response.json()

def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def memoize(fn):
    """Simple memoization decorator."""
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
