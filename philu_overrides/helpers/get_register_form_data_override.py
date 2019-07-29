# edx-platform/common/djangoapps/third_party_auth/models.py


@classmethod
def get_register_form_data(cls, pipeline_kwargs):
    """Gets dict of data to display on the register form.

    common.djangoapps.student.views.register_user uses this to populate the
    new account creation form with values supplied by the user's chosen
    provider, preventing duplicate data entry.

    Args:
        pipeline_kwargs: dict of string -> object. Keyword arguments
            accumulated by the pipeline thus far.

    Returns:
        Dict of string -> string. Keys are names of form fields; values are
        values for that field. Where there is no value, the empty string
        must be used.
    """
    # Details about the user sent back from the provider.
    details = pipeline_kwargs.get('details')

    # Get the username separately to take advantage of the de-duping logic
    # built into the pipeline. The provider cannot de-dupe because it can't
    # check the state of taken usernames in our system. Note that there is
    # technically a data race between the creation of this value and the
    # creation of the user object, so it is still possible for users to get
    # an error on submit.
    suggested_username = pipeline_kwargs.get('username')

    return {
        'email': details.get('email', ''),
        'name': details.get('fullname', ''),
        'username': suggested_username,
    }
