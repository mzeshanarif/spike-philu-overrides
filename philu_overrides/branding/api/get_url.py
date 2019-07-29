# edx-platform/lms/djangoapps/branding/api.py

def get_url(name):
    """
    Lookup and return page url, lookup is performed in the following order

    1. get url, If configuration URL override exists, return it
    2. Otherwise return the marketing URL.

    :return: string containing page url.
    """
    # If a configuration URL override exists, return it.  Otherwise return the marketing URL.
    configuration_url = get_configuration_url(name)
    if configuration_url != EMPTY_URL:
        return configuration_url

    # get marketing link, if marketing is disabled then platform url will be used instead.
    url = marketing_link(name)

    return url or EMPTY_URL
