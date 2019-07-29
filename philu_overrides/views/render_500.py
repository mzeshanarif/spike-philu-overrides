# /edx-platform/lms/djangoapps/static_template_view/views.py

def render_500(request):
    try:
        return HttpResponseServerError(render_to_string('custom_static_templates/server-error.html', {}, request=request))
    except:
        return redirect("500/")
