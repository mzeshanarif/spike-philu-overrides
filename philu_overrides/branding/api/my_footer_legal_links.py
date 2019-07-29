# edx-platform/lms/djangoapps/branding/api.py

def _footer_legal_links():
    """Return the legal footer links (e.g. terms of service). """

    links = [
        ("terms_of_service_and_honor_code", marketing_link("TOS_AND_HONOR"), _("Terms of Service & Honor Code")),
        ("privacy_policy", marketing_link("PRIVACY"), _("Privacy Policy")),
        ("accessibility_policy", marketing_link("ACCESSIBILITY"), _("Accessibility Policy")),
        ("sitemap", marketing_link("SITE_MAP"), _("Sitemap")),
        ("media_kit", marketing_link("MEDIA_KIT"), _("Media Kit")),
    ]

    # Backwards compatibility: If a combined "terms of service and honor code"
    # link isn't provided, add separate TOS and honor code links.
    tos_and_honor_link = marketing_link("TOS_AND_HONOR")
    if not (tos_and_honor_link and tos_and_honor_link != "#"):
        links.extend([
            ("terms_of_service", marketing_link("TOS"), _("Terms of Service")),
            ("honor_code", marketing_link("HONOR"), _("Honor Code")),
        ])

    return [
        {
            "name": link_name,
            "title": link_title,
            "url": link_url,
        }
        for link_name, link_url, link_title in links
        if link_url and link_url != "#"
    ]
