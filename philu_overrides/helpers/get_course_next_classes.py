def get_course_next_classes(request, course):
    """
    Method to get all upcoming reruns of a course
    """

    # imports to avoid circular dependencies
    from lms.djangoapps.courseware.access import _can_enroll_courselike
    from lms.djangoapps.courseware.views.views import registered_for_course
    from student.models import CourseEnrollment
    from opaque_keys.edx.locations import SlashSeparatedCourseKey

    courses = get_all_reruns_of_a_course(course)

    course_next_classes = []

    for _course in courses:
        course_key = SlashSeparatedCourseKey.from_deprecated_string(_course.id.__str__())
        course = get_course_by_id(course_key)
        course.course_open_date = _course.course_open_date
        registered = registered_for_course(course, request.user)

        # Used to provide context to message to student if enrollment not allowed
        can_enroll = _can_enroll_courselike(request.user, course)
        invitation_only = course.invitation_only
        is_course_full = CourseEnrollment.objects.is_course_full(course)

        # Register button should be disabled if one of the following is true:
        # - Student is already registered for course
        # - Course is already full
        # - Student cannot enroll in course
        active_reg_button = not (registered or is_course_full or not can_enroll)
        course_first_chapter_link = ""
        if request.user.is_authenticated() and request.user.is_staff:
            # imported get_course_first_chapter_link here because importing above was throwing circular exception
            from openedx.core.djangoapps.timed_notification.core import get_course_first_chapter_link
            course_first_chapter_link = get_course_first_chapter_link(_course)

        course_next_classes.append({
            'user': request.user,
            'registered': registered,
            'is_course_full': is_course_full,
            'can_enroll': can_enroll.has_access,
            'invitation_only': invitation_only,
            'course': course,
            'active_reg_button': active_reg_button,
            'course_first_chapter_link': course_first_chapter_link
        })
    return course_next_classes
