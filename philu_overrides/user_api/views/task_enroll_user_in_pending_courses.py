@task()
def task_enroll_user_in_pending_courses(data):
    user = User.objects.get(id=data['user_id'])
    _enroll_user_in_pending_courses(user)
