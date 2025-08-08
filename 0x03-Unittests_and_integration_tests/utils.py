# utils.py

import requests

def get_json(url):
    response = requests.get(url)
    return response.json()

def access_nested_map(nested_map, path):
    """Access a nested dictionary using a list of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
