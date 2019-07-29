# edx-platform/lms/djangoapps/branding/api.py

def is_enabled():
    """Check whether the branding API is enabled. """
    return BrandingApiConfig.current().enabled
