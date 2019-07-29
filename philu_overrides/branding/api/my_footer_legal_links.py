# edx-platform/lms/djangoapps/branding/api.py

def my_footer_legal_links():
    """Return the legal footer links (e.g. terms of service). """

    links = [
        ("terms_of_service_and_honor_code", "https://philanthropyu.org/terms-of-use/", _("Terms of Use"), "_blank"),
        ("privacy_policy", "https://philanthropyu.org/privacy-policy/", _("Privacy Policy"), "_blank"),
        ("faq", "https://philanthropyu.org/faq/", _("FAQ"), "_blank")
    ]

    return [
        {
            "name": link_name,
            "title": link_title,
            "url": link_url,
            "target": link_target,
        }
        for link_name, link_url, link_title, link_target in links
        if link_url and link_url != "#"
    ]
