# edx-platform/lms/djangoapps/branding/api.py

def _auth_footer_courses_communities_links():
    """Return the navigation links to display in the footer. """
    platform_name = configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME)
    return [
        {
            "name": link_name,
            "title": link_title,
            "url": link_url,
            "target": link_target,
            "class": link_class
        }
        for link_name, link_url, link_title, link_target, link_class in [
            ("explore_course", "/courses", _("Explore our Courses"), "_self", ""),
            ("communities", settings.NODEBB_ENDPOINT, _("Be part of our Communities"), "_self", "communities-link"),
        ]
        if link_url and link_url != "#"
    ]
