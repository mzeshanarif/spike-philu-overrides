# edx-platform/lms/djangoapps/branding/api.py

def get_privacy_url():
    """
    Lookup and return privacy policies page url
    """
    return get_url("PRIVACY")
