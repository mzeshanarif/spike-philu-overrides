# /edx-platform/lms/djangoapps/static_template_view/views.py

def render_404(request):
    try:
        return HttpResponseNotFound(render_to_string('custom_static_templates/404.html', {}, request=request))
    except:
        return redirect("404/")
