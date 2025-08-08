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
