# /edx-platform/lms/djangoapps/courseware/views/views.py 

@ensure_csrf_cookie
@cache_if_anonymous()
def courses(request):
    """
    Render "find courses" page.  The course selection work is done in courseware.courses.
    """
    courses_list = []
    programs_list = []
    course_discovery_meanings = getattr(settings, 'COURSE_DISCOVERY_MEANINGS', {})
    if not settings.FEATURES.get('ENABLE_COURSE_DISCOVERY'):
        courses_list = get_courses(request.user)

        if configuration_helpers.get_value("ENABLE_COURSE_SORTING_BY_START_DATE",
                                           settings.FEATURES["ENABLE_COURSE_SORTING_BY_START_DATE"]):
            courses_list = sort_by_start_date(courses_list)
        else:
            courses_list = sort_by_announcement(courses_list)

    # Getting all the programs from course-catalog service. The programs_list is being added to the context but it's
    # not being used currently in courseware/courses.html. To use this list, you need to create a custom theme that
    # overrides courses.html. The modifications to courses.html to display the programs will be done after the support
    # for edx-pattern-library is added.
    if configuration_helpers.get_value("DISPLAY_PROGRAMS_ON_MARKETING_PAGES",
                                       settings.FEATURES.get("DISPLAY_PROGRAMS_ON_MARKETING_PAGES")):
        programs_list = get_programs_data(request.user)

    if request.user.is_authenticated():
        add_tag_to_enrolled_courses(request.user, courses_list)

    return render_to_response(
        "courseware/courses.html",
        {
            'courses': courses_list,
            'course_discovery_meanings': course_discovery_meanings,
            'programs_list': programs_list
        }
    )
