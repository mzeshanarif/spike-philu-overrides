# edx-platform/lms/djangoapps/branding/api.py

def _absolute_url_staticfile(is_secure, name):
    """Construct an absolute URL to a static resource on the site.

    Arguments:
        is_secure (bool): If true, use HTTPS as the protocol.
        name (unicode): The name of the static resource to retrieve.

    Returns:
        unicode

    """
    url_path = staticfiles_storage.url(name)

    # In production, the static files URL will be an absolute
    # URL pointing to a CDN.  If this happens, we can just
    # return the URL.
    if urlparse.urlparse(url_path).netloc:
        return url_path

    # For local development, the returned URL will be relative,
    # so we need to make it absolute.
    return _absolute_url(is_secure, url_path)
