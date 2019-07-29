# /edx-platform/lms/djangoapps/static_template_view/views.py

def render_500(request):
    return HttpResponseServerError(render_to_string('static_templates/server-error.html', {}, request=request))
