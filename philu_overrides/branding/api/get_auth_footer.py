# edx-platform/lms/djangoapps/branding/api.py

def get_auth_footer(is_secure=True):
    """ Override default get_footer method & add link for after authentication pages"""
    return {
        "copyright": _auth_footer_copyright(),
        "social_links": _auth_footer_social_links(),
        "navigation_links": _auth_footer_navigation_links(),
        "courses_communities_links": _auth_footer_courses_communities_links(),
        "legal_links": _auth_footer_legal_links(),
    }
