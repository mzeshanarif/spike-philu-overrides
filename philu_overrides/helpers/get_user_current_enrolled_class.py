def get_user_current_enrolled_class(request, course):
    """
    Method to get an ongoing user enrolled course. A course that meets the following criteria
    => start date <= today
    => end date > today
    => user is enrolled
    """
    from datetime import datetime
    from django.core.urlresolvers import reverse
    from opaque_keys.edx.locations import SlashSeparatedCourseKey
    from common.djangoapps.student.views import get_course_related_keys
    from student.models import CourseEnrollment
    from course_action_state.models import CourseRerunState

    all_course_reruns = [crs.course_key for crs in CourseRerunState.objects.filter(
        source_course_key=course.id, action="rerun", state="succeeded")] + [course.id]
    current_time = datetime.utcnow().replace(tzinfo=utc)
    current_class = get_course_current_class(all_course_reruns, current_time)

    current_enrolled_class = False
    if current_class:
        current_enrolled_class = CourseEnrollment.is_enrolled(request.user, current_class.id)

    current_enrolled_class_target = ''
    if current_enrolled_class:
        course_open_date = current_class.course_open_date
        course_key = SlashSeparatedCourseKey.from_deprecated_string(current_class.id.__str__())
        current_class = get_course_by_id(course_key)
        current_class.course_open_date = course_open_date
        first_chapter_url, first_section = get_course_related_keys(request, current_class)
        current_enrolled_class_target = reverse('courseware_section',
                                                args=[current_class.id.to_deprecated_string(),
                                                      first_chapter_url, first_section])

    return current_class, current_enrolled_class, current_enrolled_class_target
