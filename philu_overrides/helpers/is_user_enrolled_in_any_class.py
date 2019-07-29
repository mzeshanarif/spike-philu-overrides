def is_user_enrolled_in_any_class(course_current_class, course_next_classes):
    next_reg_classes = filter(lambda next_class: next_class['registered'], course_next_classes)
    return bool(course_current_class or next_reg_classes)
