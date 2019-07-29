def has_access_custom(course):
    """ User can enroll if current time is between enrollment start and end date """
    current_time = datetime.utcnow().replace(tzinfo=utc)
    if not course.enrollment_start or not course.enrollment_end:
        return False

    if course.enrollment_start < current_time < course.enrollment_end:
        return True
    else:
        return False
