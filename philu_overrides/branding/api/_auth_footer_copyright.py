# edx-platform/lms/djangoapps/branding/api.py

def _auth_footer_copyright():
    """Return the copyright to display in the footer.

    Returns: unicode

    """
    return _(
        # Translators: 'EdX', 'edX', and 'Open edX' are trademarks of 'edX Inc.'.
        # Please do not translate any of these trademarks and company names.
        u"\u00A9 {org_name}.  All rights reserved except where noted.  "
        u"EdX, Open edX and the edX and Open EdX logos are registered trademarks "
        u"or trademarks of edX Inc."
    ).format(org_name=configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME))
