# edx-platform/common/djangoapps/student/helpers.py

def get_next_url_for_login_page_override(request):
    """
    NOTE*: We override this method to tackle alquity redirection scenarios
    Determine the URL to redirect to following login/registration/third_party_auth

    The user is currently on a login or registration page.
    If 'course_id' is set, or other POST_AUTH_PARAMS, we will need to send the user to the
    /account/finish_auth/ view following login, which will take care of auto-enrollment in
    the specified course.

    Otherwise, we go to the ?next= query param or to the dashboard if nothing else is
    specified.
    """
    import urllib
    from django.core.urlresolvers import reverse, NoReverseMatch
    from django.utils import http
    from lms.djangoapps.onboarding.helpers import get_alquity_community_url
    import logging
    log = logging.getLogger(__name__)

    redirect_to = request.GET.get('next', None)

    # sanity checks for alquity specific users
    if redirect_to == 'alquity' and request.path == '/register':
        if request.user.is_authenticated():
            return get_alquity_community_url()
        return reverse('dashboard')

    if redirect_to == 'alquity' and request.path == '/login':
        return get_alquity_community_url()


    # if we get a redirect parameter, make sure it's safe. If it's not, drop the
    # parameter.
    if redirect_to and not http.is_safe_url(redirect_to):
        log.error(
            u'Unsafe redirect parameter detected: %(redirect_to)r',
            {"redirect_to": redirect_to}
        )
        redirect_to = None

    course_id = request.GET.get('course_id', None)
    if not redirect_to:
        try:
            if course_id:
                redirect_to = reverse('info', args=[course_id])
            else:
                redirect_to = reverse('dashboard')
        except NoReverseMatch:
            redirect_to = reverse('home')
    if any(param in request.GET for param in POST_AUTH_PARAMS):
        # Before we redirect to next/dashboard, we need to handle auto-enrollment:
        params = [(param, request.GET[param]) for param in POST_AUTH_PARAMS if param in request.GET]
        params.append(('next', redirect_to))  # After auto-enrollment, user will be sent to payment page or to this URL
        redirect_to = '{}?{}'.format(reverse('finish_auth'), urllib.urlencode(params))
        # Note: if we are resuming a third party auth pipeline, then the next URL will already
        # be saved in the session as part of the pipeline state. That URL will take priority
        # over this one.
    return redirect_to
