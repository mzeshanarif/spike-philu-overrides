# /edx-platform/lms/djangoapps/courseware/views/views.py

@ensure_csrf_cookie
@cache_if_anonymous()
def course_about(request, course_id):
    """
    Display the course's about page.

    Assumes the course_id is in a valid format.
    """

    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    if hasattr(course_key, 'ccx'):
        # if un-enrolled/non-registered user try to access CCX (direct for registration)
        # then do not show him about page to avoid self registration.
        # Note: About page will only be shown to user who is not register. So that he can register. But for
        # CCX only CCX coach can enroll students.
        return redirect(reverse('dashboard'))

    with modulestore().bulk_operations(course_key):
        permission = get_permission_for_course_about()
        course = get_course_with_access(request.user, permission, course_key)
        course_details = CourseDetails.populate(course)
        modes = CourseMode.modes_for_course_dict(course_key)

        if configuration_helpers.get_value('ENABLE_MKTG_SITE', settings.FEATURES.get('ENABLE_MKTG_SITE', False)):
            return redirect(reverse('info', args=[course.id.to_deprecated_string()]))

        registered = registered_for_course(course, request.user)

        staff_access = bool(has_access(request.user, 'staff', course))
        studio_url = get_studio_url(course, 'settings/details')

        if has_access(request.user, 'load', course):
            first_chapter_url, first_section = get_course_related_keys(request, course)
            course_target = reverse('courseware_section', args=[course.id.to_deprecated_string(), first_chapter_url,
                                                                first_section])
        else:
            course_target = reverse('about_course', args=[course.id.to_deprecated_string()])

        show_courseware_link = bool(
            (
                has_access(request.user, 'load', course) and
                has_access(request.user, 'view_courseware_with_prerequisites', course)
            ) or settings.FEATURES.get('ENABLE_LMS_MIGRATION')
        )

        # Note: this is a flow for payment for course registration, not the Verified Certificate flow.
        in_cart = False
        reg_then_add_to_cart_link = ""

        _is_shopping_cart_enabled = is_shopping_cart_enabled()
        if _is_shopping_cart_enabled:
            if request.user.is_authenticated():
                cart = shoppingcart.models.Order.get_cart_for_user(request.user)
                in_cart = shoppingcart.models.PaidCourseRegistration.contained_in_order(cart, course_key) or \
                    shoppingcart.models.CourseRegCodeItem.contained_in_order(cart, course_key)

            reg_then_add_to_cart_link = "{reg_url}?course_id={course_id}&enrollment_action=add_to_cart".format(
                reg_url=reverse('register_user'), course_id=urllib.quote(str(course_id))
            )

        # If the ecommerce checkout flow is enabled and the mode of the course is
        # professional or no id professional, we construct links for the enrollment
        # button to add the course to the ecommerce basket.
        ecomm_service = EcommerceService()
        ecommerce_checkout = ecomm_service.is_enabled(request.user)
        ecommerce_checkout_link = ''
        ecommerce_bulk_checkout_link = ''
        professional_mode = None
        is_professional_mode = CourseMode.PROFESSIONAL in modes or CourseMode.NO_ID_PROFESSIONAL_MODE in modes
        if ecommerce_checkout and is_professional_mode:
            professional_mode = modes.get(CourseMode.PROFESSIONAL, '') or \
                modes.get(CourseMode.NO_ID_PROFESSIONAL_MODE, '')
            if professional_mode.sku:
                ecommerce_checkout_link = ecomm_service.checkout_page_url(professional_mode.sku)
            if professional_mode.bulk_sku:
                ecommerce_bulk_checkout_link = ecomm_service.checkout_page_url(professional_mode.bulk_sku)

        # Find the minimum price for the course across all course modes
        registration_price = CourseMode.min_course_price_for_currency(
            course_key,
            settings.PAID_COURSE_REGISTRATION_CURRENCY[0]
        )
        course_price = get_cosmetic_display_price(course, registration_price)

        # Determine which checkout workflow to use -- LMS shoppingcart or Otto basket
        can_add_course_to_cart = _is_shopping_cart_enabled and registration_price and not ecommerce_checkout_link

        # Used to provide context to message to student if enrollment not allowed
        can_enroll = bool(has_access(request.user, 'enroll', course))
        invitation_only = course.invitation_only
        is_course_full = CourseEnrollment.objects.is_course_full(course)

        # Register button should be disabled if one of the following is true:
        # - Student is already registered for course
        # - Course is already full
        # - Student cannot enroll in course
        active_reg_button = not(registered or is_course_full or not can_enroll)

        is_shib_course = uses_shib(course)

        # get prerequisite courses display names
        pre_requisite_courses = get_prerequisite_courses_display(course)

        # Overview
        overview = CourseOverview.get_from_id(course.id)

        context = {
            'course': course,
            'course_details': course_details,
            'staff_access': staff_access,
            'studio_url': studio_url,
            'registered': registered,
            'course_target': course_target,
            'is_cosmetic_price_enabled': settings.FEATURES.get('ENABLE_COSMETIC_DISPLAY_PRICE'),
            'course_price': course_price,
            'in_cart': in_cart,
            'ecommerce_checkout': ecommerce_checkout,
            'ecommerce_checkout_link': ecommerce_checkout_link,
            'ecommerce_bulk_checkout_link': ecommerce_bulk_checkout_link,
            'professional_mode': professional_mode,
            'reg_then_add_to_cart_link': reg_then_add_to_cart_link,
            'show_courseware_link': show_courseware_link,
            'is_course_full': is_course_full,
            'can_enroll': can_enroll,
            'invitation_only': invitation_only,
            'active_reg_button': active_reg_button,
            'is_shib_course': is_shib_course,
            # We do not want to display the internal courseware header, which is used when the course is found in the
            # context. This value is therefor explicitly set to render the appropriate header.
            'disable_courseware_header': True,
            'can_add_course_to_cart': can_add_course_to_cart,
            'cart_link': reverse('shoppingcart.views.show_cart'),
            'pre_requisite_courses': pre_requisite_courses,
            'course_image_urls': overview.image_urls,
        }
        inject_coursetalk_keys_into_context(context, course_key)

        return render_to_response('courseware/course_about.html', context)
