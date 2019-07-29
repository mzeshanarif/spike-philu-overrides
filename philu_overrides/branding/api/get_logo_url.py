# edx-platform/lms/djangoapps/branding/api.py

def get_logo_url(is_secure=True):
    """
    Return the url for the branded logo image to be used
    Arguments:
        is_secure (bool): If true, use HTTPS as the protocol.
    """

    # if the configuration has an overide value for the logo_image_url
    # let's use that
    image_url = configuration_helpers.get_value('logo_image_url')
    if image_url:
        return _absolute_url_staticfile(
            is_secure=is_secure,
            name=image_url,
        )

    # otherwise, use the legacy means to configure this
    university = configuration_helpers.get_value('university')

    if university:
        return staticfiles_storage.url('images/{uni}-on-edx-logo.png'.format(uni=university))
    else:
        return staticfiles_storage.url('images/logo.png')
