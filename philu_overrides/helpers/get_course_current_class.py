def get_course_current_class(all_course_reruns, current_time):
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    from openedx.features.course_card.helpers import get_course_open_date
    course = CourseOverview.objects.select_related('image_set').filter(
        id__in=all_course_reruns, start__lte=current_time, end__gte=current_time).order_by('-start').first()

    if course:
        course_open_date = get_course_open_date(course)

        if course.start <= current_time:
            course.course_open_date = course_open_date
            return course
        else:
            return None
