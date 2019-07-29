def course_auto_enroll(request, course_id):
    """
    Auto enrolls any authenticated user in the course with course_id
    """
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course_custom_settings = get_course_custom_settings(course_id)

    if request.user.is_anonymous():
        return redirect(get_alquity_community_url())

    if course_custom_settings.auto_enroll:
        CourseEnrollment.enroll(request.user, course_key)

    return redirect('/courses/{}/about?ref=alquity'.format(course_id))
