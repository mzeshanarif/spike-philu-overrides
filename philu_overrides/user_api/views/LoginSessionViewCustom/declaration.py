class LoginSessionView(APIView):
    """HTTP end-points for logging in users. """

    # This end-point is available to anonymous users,
    # so do not require authentication.
    authentication_classes = []
