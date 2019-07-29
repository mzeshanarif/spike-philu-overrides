# edx-platform/lms/djangoapps/branding/api.py

def _auth_footer_navigation_links():
    """Return the navigation links to display in the footer. """
    platform_name = configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME)
    return [
        {
            "name": link_name,
            "title": link_title,
            "url": link_url,
            "target": link_target,
        }
        for link_name, link_url, link_title, link_target in [
            ("about", "https://philanthropyu.org/about-us/our-story/", _("About Philanthropy University"), "_blank")
        ]
        if link_url and link_url != "#"
    ]
