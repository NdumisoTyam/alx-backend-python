def access_nested_map(nested_map, path):
    """
    Traverse a nested map (dicts within dicts) by following the sequence of keys
    in `path`, and return the value found at the end.

    Args:
        nested_map (dict): A potentially nested dictionary.
        path (tuple): A sequence of keys to follow in order.

    Returns:
        The value obtained by successively indexing into nested_map with each key.

    Raises:
        KeyError: If any key in the path is not present.
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current