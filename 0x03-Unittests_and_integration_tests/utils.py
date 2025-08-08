import requests
from functools import wraps

def get_json(url):
    """
    Fetch JSON content from a given URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The parsed JSON response.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def access_nested_map(nested_map, path):
    """
    Retrieve a value from a nested dictionary using a sequence of keys.

    Args:
        nested_map (dict): The dictionary to traverse.
        path (list): A list of keys representing the path to the desired value.

    Returns:
        The value found at the end of the path.

    Raises:
        KeyError: If any key in the path is not found in the current level of the dictionary.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def memoize(fn):
    """
    Decorator that caches the result of a method call.

    The result is stored as a private attribute on the instance,
    so subsequent calls return the cached value.

    Args:
        fn (Callable): The method to memoize.

    Returns:
        Callable: The wrapped method with caching.
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
