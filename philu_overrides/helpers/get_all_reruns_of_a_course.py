def get_all_reruns_of_a_course(course):
    """
    :param course:
    :return reruns:
    """
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    from course_action_state.models import CourseRerunState
    from openedx.features.course_card.helpers import get_course_open_date
    courses = []
    current_time = datetime.utcnow().replace(tzinfo=utc)
    course_rerun_states = [crs.course_key for crs in CourseRerunState.objects.filter(
        source_course_key=course.id, action="rerun", state="succeeded")] + [course.id]
    course_rerun_objects = CourseOverview.objects.select_related('image_set').filter(
        id__in=course_rerun_states).order_by('start')
    for course_run in course_rerun_objects:

        course_open_date = get_course_open_date(course_run)
        if course_run.start > current_time:
            course_run.course_open_date = course_open_date
            courses.append(course_run)

    return courses
