# edx-platform/lms/djangoapps/branding/api.py

def _auth_footer_social_links():
    """Return the social media links to display in the footer.

    Returns: list

    """
    platform_name = configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME)
    links = []

    for social_name in settings.SOCIAL_MEDIA_FOOTER_NAMES:
        display = settings.SOCIAL_MEDIA_FOOTER_DISPLAY.get(social_name, {})
        links.append(
            {
                "name": social_name,
                "title": unicode(display.get("title", "")),
                "url": settings.SOCIAL_MEDIA_FOOTER_URLS.get(social_name, "#"),
                "icon-class": display.get("icon", ""),
                "action": unicode(display.get("action", "")).format(platform_name=platform_name),
            }
        )
    return links
