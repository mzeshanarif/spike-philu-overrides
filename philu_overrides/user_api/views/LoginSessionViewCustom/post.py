    @method_decorator(require_post_params(["email", "password"]))
    @method_decorator(csrf_protect)
    def post(self, request):
        """Log in a user.

        You must send all required form fields with the request.

        You can optionally send an `analytics` param with a JSON-encoded
        object with additional info to include in the login analytics event.
        Currently, the only supported field is "enroll_course_id" to indicate
        that the user logged in while enrolling in a particular course.

        Arguments:
            request (HttpRequest)

        Returns:
            HttpResponse: 200 on success
            HttpResponse: 400 if the request is not valid.
            HttpResponse: 403 if authentication failed.
                403 with content "third-party-auth" if the user
                has successfully authenticated with a third party provider
                but does not have a linked account.
            HttpResponse: 302 if redirecting to another page.

        Example Usage:

            POST /user_api/v1/login_session
            with POST params `email`, `password`, and `remember`.

            200 OK

        """
        # For the initial implementation, shim the existing login view
        # from the student Django app.
        from student.views import login_user
        return shim_student_view(login_user, check_logged_in=True)(request)
