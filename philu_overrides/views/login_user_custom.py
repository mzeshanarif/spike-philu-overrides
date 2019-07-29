# /edx-platform/common/djangoapps/student/views.py

# Need different levels of logging
@ensure_csrf_cookie
def login_user_custom(request, error=""):  # pylint: disable=too-many-statements,unused-argument
    """AJAX request to log in the user."""

    backend_name = None
    email = None
    password = None
    redirect_url = None
    response = None
    running_pipeline = None
    third_party_auth_requested = third_party_auth.is_enabled() and pipeline.running(request)
    third_party_auth_successful = False
    trumped_by_first_party_auth = bool(request.POST.get('email')) or bool(request.POST.get('password'))
    user = None
    platform_name = configuration_helpers.get_value("platform_name", settings.PLATFORM_NAME)

    if third_party_auth_requested and not trumped_by_first_party_auth:
        # The user has already authenticated via third-party auth and has not
        # asked to do first party auth by supplying a username or password. We
        # now want to put them through the same logging and cookie calculation
        # logic as with first-party auth.
        running_pipeline = pipeline.get(request)
        username = running_pipeline['kwargs'].get('username')
        backend_name = running_pipeline['backend']
        third_party_uid = running_pipeline['kwargs']['uid']
        requested_provider = provider.Registry.get_from_pipeline(running_pipeline)

        try:
            user = pipeline.get_authenticated_user(requested_provider, username, third_party_uid)
            third_party_auth_successful = True
        except User.DoesNotExist:
            AUDIT_LOG.warning(
                u"Login failed - user with username {username} has no social auth "
                "with backend_name {backend_name}".format(
                    username=username, backend_name=backend_name)
            )
            message = _(
                "You've successfully logged into your {provider_name} account, "
                "but this account isn't linked with an {platform_name} account yet."
            ).format(
                platform_name=platform_name,
                provider_name=requested_provider.name,
            )
            message += "<br/><br/>"
            message += _(
                "Use your {platform_name} username and password to log into {platform_name} below, "
                "and then link your {platform_name} account with {provider_name} from your dashboard."
            ).format(
                platform_name=platform_name,
                provider_name=requested_provider.name,
            )
            message += "<br/><br/>"
            message += _(
                "If you don't have an {platform_name} account yet, "
                "click <strong>Register</strong> at the top of the page."
            ).format(
                platform_name=platform_name
            )

            return HttpResponse(message, content_type="text/plain", status=403)

    else:

        if 'email' not in request.POST or 'password' not in request.POST:
            return JsonResponse({
                "success": False,
                # TODO: User error message
                "value": _('There was an error receiving your login information. Please email us.'),
            })  # TODO: this should be status code 400

        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            if settings.FEATURES['SQUELCH_PII_IN_LOGS']:
                AUDIT_LOG.warning(u"Login failed - Unknown user email")
            else:
                AUDIT_LOG.warning(u"Login failed - Unknown user email: {0}".format(email))

    # check if the user has a linked shibboleth account, if so, redirect the user to shib-login
    # This behavior is pretty much like what gmail does for shibboleth.  Try entering some @stanford.edu
    # address into the Gmail login.
    if settings.FEATURES.get('AUTH_USE_SHIB') and user:
        try:
            eamap = ExternalAuthMap.objects.get(user=user)
            if eamap.external_domain.startswith(openedx.core.djangoapps.external_auth.views.SHIBBOLETH_DOMAIN_PREFIX):
                return JsonResponse({
                    "success": False,
                    "redirect": reverse('shib-login'),
                })  # TODO: this should be status code 301  # pylint: disable=fixme
        except ExternalAuthMap.DoesNotExist:
            # This is actually the common case, logging in user without external linked login
            AUDIT_LOG.info(u"User %s w/o external auth attempting login", user)

    # see if account has been locked out due to excessive login failures
    user_found_by_email_lookup = user
    if user_found_by_email_lookup and LoginFailures.is_feature_enabled():
        if LoginFailures.is_user_locked_out(user_found_by_email_lookup):
            lockout_message = _('This account has been temporarily locked due '
                                'to excessive login failures. Try again later.')
            return JsonResponse({
                "success": False,
                "value": lockout_message,
            })  # TODO: this should be status code 429  # pylint: disable=fixme

    # see if the user must reset his/her password due to any policy settings
    if user_found_by_email_lookup and PasswordHistory.should_user_reset_password_now(user_found_by_email_lookup):
        return JsonResponse({
            "success": False,
            "value": _('Your password has expired due to password policy on this account. You must '
                       'reset your password before you can log in again. Please click the '
                       '"Forgot Password" link on this page to reset your password before logging in again.'),
        })  # TODO: this should be status code 403  # pylint: disable=fixme

    # if the user doesn't exist, we want to set the username to an invalid
    # username so that authentication is guaranteed to fail and we can take
    # advantage of the ratelimited backend
    username = user.username if user else ""

    if not third_party_auth_successful:
        try:
            user = authenticate(username=username, password=password, request=request)
        # this occurs when there are too many attempts from the same IP address
        except RateLimitException:
            return JsonResponse({
                "success": False,
                "value": _('Too many failed login attempts. Try again later.'),
            })  # TODO: this should be status code 429  # pylint: disable=fixme

    if user is None:
        # tick the failed login counters if the user exists in the database
        if user_found_by_email_lookup and LoginFailures.is_feature_enabled():
            LoginFailures.increment_lockout_counter(user_found_by_email_lookup)

        # if we didn't find this username earlier, the account for this email
        # doesn't exist, and doesn't have a corresponding password
        if username != "":
            if settings.FEATURES['SQUELCH_PII_IN_LOGS']:
                loggable_id = user_found_by_email_lookup.id if user_found_by_email_lookup else "<unknown>"
                AUDIT_LOG.warning(u"Login failed - password for user.id: {0} is invalid".format(loggable_id))
            else:
                AUDIT_LOG.warning(u"Login failed - password for {0} is invalid".format(email))
        return JsonResponse({
            "success": False,
            "value": _('Email or password is incorrect.'),
        })  # TODO: this should be status code 400  # pylint: disable=fixme

    # successful login, clear failed login attempts counters, if applicable
    if LoginFailures.is_feature_enabled():
        LoginFailures.clear_lockout_counter(user)

    # Track the user's sign in
    if hasattr(settings, 'LMS_SEGMENT_KEY') and settings.LMS_SEGMENT_KEY:
        tracking_context = tracker.get_tracker().resolve_context()
        analytics.identify(
            user.id,
            {
                'email': email,
                'username': username
            },
            {
                # Disable MailChimp because we don't want to update the user's email
                # and username in MailChimp on every page load. We only need to capture
                # this data on registration/activation.
                'MailChimp': False
            }
        )

        analytics.track(
            user.id,
            "edx.bi.user.account.authenticated",
            {
                'category': "conversion",
                'label': request.POST.get('course_id'),
                'provider': None
            },
            context={
                'ip': tracking_context.get('ip'),
                'Google Analytics': {
                    'clientId': tracking_context.get('client_id')
                }
            }
        )

    if user is not None and user.is_active:
        try:
            # We do not log here, because we have a handler registered
            # to perform logging on successful logins.
            login(request, user)
            if request.POST.get('remember') == 'true':
                request.session.set_expiry(604800)
                log.debug("Setting user session to never expire")
            else:
                request.session.set_expiry(0)
        except Exception as exc:  # pylint: disable=broad-except
            AUDIT_LOG.critical("Login failed - Could not create session. Is memcached running?")
            log.critical("Login failed - Could not create session. Is memcached running?")
            log.exception(exc)
            raise

        redirect_url = None  # The AJAX method calling should know the default destination upon success
        if third_party_auth_successful:
            redirect_url = pipeline.get_complete_url(backend_name)

        response = JsonResponse({
            "success": True,
            "redirect_url": redirect_url,
        })

        # Ensure that the external marketing site can
        # detect that the user is logged in.
        return set_logged_in_cookies(request, response, user)

    if settings.FEATURES['SQUELCH_PII_IN_LOGS']:
        AUDIT_LOG.warning(u"Login failed - Account not active for user.id: {0}, resending activation".format(user.id))
    else:
        AUDIT_LOG.warning(u"Login failed - Account not active for user {0}, resending activation".format(username))

    reactivation_email_for_user_custom(request, user)
    not_activated_msg = _("Before you sign in, you need to activate your account. We have sent you an "
                          "email message with instructions for activating your account.")
    return JsonResponse({
        "success": False,
        "value": not_activated_msg,
    })  # TODO: this should be status code 400  # pylint: disable=fixme
