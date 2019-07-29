# edx-platform/lms/djangoapps/branding/api.py

def get_non_auth_footer(is_secure=True):
    """ Override default get_footer method """

    return {
        "copyright": _footer_copyright(),
        "social_links": _footer_social_links(),
        "navigation_links": _footer_navigation_links(),
        "legal_links": my_footer_legal_links(),
    }
