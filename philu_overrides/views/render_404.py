# /edx-platform/lms/djangoapps/static_template_view/views.py

def render_404(request):
    return HttpResponseNotFound(render_to_string('static_templates/404.html', {}, request=request))