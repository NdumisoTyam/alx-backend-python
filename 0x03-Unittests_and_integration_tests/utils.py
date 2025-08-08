import requests

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
