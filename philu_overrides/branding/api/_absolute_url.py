# edx-platform/lms/djangoapps/branding/api.py

def _absolute_url(is_secure, url_path):
    """Construct an absolute URL back to the site.

    Arguments:
        is_secure (bool): If true, use HTTPS as the protocol.
        url_path (unicode): The path of the URL.

    Returns:
        unicode

    """
    site_name = configuration_helpers.get_value('SITE_NAME', settings.SITE_NAME)
    parts = ("https" if is_secure else "http", site_name, url_path, '', '', '')
    return urlparse.urlunparse(parts)
