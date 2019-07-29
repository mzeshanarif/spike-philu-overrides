# /edx-platform/openedx/core/djangoapps/user_api/views.py

class RegistrationView(APIView):
    """HTTP end-points for creating a new user. """

    DEFAULT_FIELDS = ["email", "username", "password"]

    EXTRA_FIELDS = [

        "first_name",
        "last_name",
        "city",
        "state",
        "country",
        "gender",
        "year_of_birth",
        "level_of_education",
        "company",
        "title",
        "mailing_address",
        "goals",
        "terms_of_service",
        "honor_code"
    ]

    # This end-point is available to anonymous users,
    # so do not require authentication.
    authentication_classes = []