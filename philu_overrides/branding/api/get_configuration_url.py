# edx-platform/lms/djangoapps/branding/api.py

def get_configuration_url(name):
    """
    Look up and return the value for given url name in configuration.
    URLs are saved in "urls" dictionary inside configuration.

    Return 'EMPTY_URL' if given url name is not defined in configuration urls.
    """
    urls = configuration_helpers.get_value("urls", default={})
    return urls.get(name) or EMPTY_URL
