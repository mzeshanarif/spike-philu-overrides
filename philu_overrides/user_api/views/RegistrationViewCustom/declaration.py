# /edx-platform/openedx/core/djangoapps/user_api/views.py

class RegistrationViewCustom(RegistrationView):
    """HTTP custom end-points for creating a new user. """
    THIRD_PARTY_OVERRIDE_FIELDS = RegistrationView.DEFAULT_FIELDS + ["first_name", "last_name"]
