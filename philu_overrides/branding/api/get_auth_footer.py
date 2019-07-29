# edx-platform/lms/djangoapps/branding/api.py

def get_footer(is_secure=True):
    """Retrieve information used to render the footer.

    This will handle both the OpenEdX and EdX.org versions
    of the footer.  All user-facing text is internationalized.

    Currently, this does NOT support theming.

    Keyword Arguments:
        is_secure (bool): If True, use https:// in URLs.

    Returns: dict

    Example:
    >>> get_footer()
    {
        "copyright": "(c) 2015 EdX Inc",
        "logo_image": "http://www.example.com/logo.png",
        "social_links": [
            {
                "name": "facebook",
                "title": "Facebook",
                "url": "http://www.facebook.com/example",
                "icon-class": "fa-facebook-square",
                "action": "Sign up on Facebook!"
            },
            ...
        ],
        "navigation_links": [
            {
                "name": "about",
                "title": "About",
                "url": "http://www.example.com/about.html"
            },
            ...
        ],
        "mobile_links": [
            {
                "name": "apple",
                "title": "Apple",
                "url": "http://store.apple.com/example_app",
                "image": "http://example.com/static/apple_logo.png"
            },
            ...
        ],
        "legal_links": [
            {
                "url": "http://example.com/terms-of-service.html",
                "name": "terms_of_service",
                "title': "Terms of Service"
            },
            # ...
        ],
        "openedx_link": {
            "url": "http://open.edx.org",
            "title": "Powered by Open edX",
            "image": "http://example.com/openedx.png"
        }
    }

    """
    return {
        "copyright": _footer_copyright(),
        "logo_image": _footer_logo_img(is_secure),
        "social_links": _footer_social_links(),
        "navigation_links": _footer_navigation_links(),
        "mobile_links": _footer_mobile_links(is_secure),
        "legal_links": _footer_legal_links(),
        "openedx_link": _footer_openedx_link(),
    }
