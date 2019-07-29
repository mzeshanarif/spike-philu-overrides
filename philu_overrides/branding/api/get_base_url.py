# edx-platform/lms/djangoapps/branding/api.py

def get_base_url(is_secure):
    """
    Return Base URL for site.
    Arguments:
        is_secure (bool): If true, use HTTPS as the protocol.
    """
    return _absolute_url(is_secure=is_secure, url_path="")
