import re


def update_params(original_return, add_params):
    """Insert additional params to dicts."""
    if isinstance(original_return, list):
        original_return = [{**i, **add_params} for i in original_return]
    elif isinstance(original_return, dict):
        original_return.update(add_params)
    return original_return


def format_url_for_search(url):
    if re.search("\?", url):
        url = url + "&"
    else:
        url = url + "?"
    if not re.search("[w]s=\d+", url):
        url = url + "s=104"
    if re.search("\?", url):
        url = url + "&"
    else:
        url = url + "?"
    if not re.search("[&|?]localPriority=\d+", url):
        url = url + "localPriority=1"
    return url
