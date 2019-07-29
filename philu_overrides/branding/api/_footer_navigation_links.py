# edx-platform/lms/djangoapps/branding/api.py

def _footer_navigation_links():
    """Return the navigation links to display in the footer. """
    platform_name = configuration_helpers.get_value('platform_name', settings.PLATFORM_NAME)
    return [
        {
            "name": link_name,
            "title": link_title,
            "url": link_url,
        }
        for link_name, link_url, link_title in [
            ("about", marketing_link("ABOUT"), _("About")),
            ("enterprise", marketing_link("ENTERPRISE"),
             _("{platform_name} for Business").format(platform_name=platform_name)),
            ("blog", marketing_link("BLOG"), _("Blog")),
            ("news", marketing_link("NEWS"), _("News")),
            ("help-center", settings.SUPPORT_SITE_LINK, _("Help Center")),
            ("contact", marketing_link("CONTACT"), _("Contact")),
            ("careers", marketing_link("CAREERS"), _("Careers")),
            ("donate", marketing_link("DONATE"), _("Donate")),
        ]
        if link_url and link_url != "#"
    ]
