# /edx-platform/lms/djangoapps/courseware/views/views.py

@ensure_csrf_cookie
@cache_if_anonymous('share_after_enroll',)
def course_about(request, course_id):
    """
    Display the course's about page.

    Assumes the course_id is in a valid format.
    """

    import urllib
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    from util.milestones_helpers import get_prerequisite_courses_display
    from openedx.core.djangoapps.models.course_details import CourseDetails
    from commerce.utils import EcommerceService
    from course_modes.models import CourseMode
    from lms.djangoapps.courseware.access_utils import ACCESS_DENIED
    from lms.djangoapps.courseware.views.views import registered_for_course, get_cosmetic_display_price
    from lms.djangoapps.courseware.courses import (
        get_courses,
        get_permission_for_course_about,
        get_course_overview_with_access,
        get_course_with_access,
        get_studio_url,
        sort_by_start_date,
        get_course_by_id,
        sort_by_announcement
    )
    from lms.envs.common import DEFAULT_IMAGE_NAME
    import shoppingcart
    from shoppingcart.utils import is_shopping_cart_enabled
    from openedx.core.djangoapps.coursetalk.helpers import inject_coursetalk_keys_into_context

    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    if hasattr(course_key, 'ccx'):
        # if un-enrolled/non-registered user try to access CCX (direct for registration)
        # then do not show him about page to avoid self registration.
        # Note: About page will only be shown to user who is not register. So that he can register. But for
        # CCX only CCX coach can enroll students.
        return redirect(reverse('dashboard'))

    with modulestore().bulk_operations(course_key):
        course = get_course_by_id(course_key)
        modes = CourseMode.modes_for_course_dict(course_key)

        if configuration_helpers.get_value('ENABLE_MKTG_SITE', settings.FEATURES.get('ENABLE_MKTG_SITE', False)):
            return redirect(reverse('info', args=[course.id.to_deprecated_string()]))

        staff_access = bool(has_access(request.user, 'staff', course))
        studio_url = get_studio_url(course, 'settings/details')

        if not staff_access and course.invitation_only and not CourseEnrollment.is_enrolled(request.user, course.id):
            raise Http404("Course not accessible: {}.".format(unicode(course.id)))

        # Note: this is a flow for payment for course registration, not the Verified Certificate flow.
        # in_cart = False
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
        # ecommerce_bulk_checkout_link = ''
        # professional_mode = None
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

        invitation_only = course.invitation_only

        # get prerequisite courses display names
        pre_requisite_courses = get_prerequisite_courses_display(course)

        # Overview
        overview = CourseOverview.get_from_id(course.id)

        course_next_classes = get_course_next_classes(request, course)
        current_class, user_current_enrolled_class, current_enrolled_class_target = get_user_current_enrolled_class(
            request, course)
        can_enroll = _can_enroll_courselike(request.user, current_class) if current_class else ACCESS_DENIED

        if current_class:
            if isinstance(current_class, CourseOverview):
                course_open_date = current_class.course_open_date
                current_class = get_course_by_id(current_class.id)
                current_class.course_open_date = course_open_date

            course_details = CourseDetails.populate(current_class)
        else:
            course_details = CourseDetails.populate(course)

        is_enrolled_in_any_class = is_user_enrolled_in_any_class(user_current_enrolled_class, course_next_classes)
        # Alquity specific check
        is_alquity = True if request.GET.get('ref') == 'alquity' else False

        custom_settings = get_course_custom_settings(course.id)
        meta_tags = custom_settings.get_course_meta_tags()

        meta_tags['description'] = meta_tags['description'] or course_details.short_description
        meta_tags['og:description'] = meta_tags['description']

        meta_tags['title'] = meta_tags['title'] or course_details.title or course.display_name
        meta_tags['og:title'] = meta_tags['title']
        meta_tags['addthis:title'] = ENROLL_SHARE_TITLE_FORMAT.format(course.display_name)

        if request.GET.get('share_after_enroll') == 'true':
            meta_tags['og:title'] = 'Join me in this free online course.'
            meta_tags['og:description'] = ENROLL_SHARE_DESC_FORMAT.format(course.display_name)

        if course_details.banner_image_name != DEFAULT_IMAGE_NAME:
            meta_tags['image'] = settings.LMS_ROOT_URL + course_details.banner_image_asset_path

        social_sharing_urls = get_social_sharing_urls(url_query_cleaner(request.build_absolute_uri()), meta_tags)

        context = {
            'course': course,
            'course_details': course_details,
            'course_next_classes': course_next_classes,
            'current_class': current_class,
            'can_user_enroll': can_enroll.has_access,
            'user_current_enrolled_class': user_current_enrolled_class,
            'is_user_enrolled_in_any_class': is_enrolled_in_any_class,
            'current_enrolled_class_target': current_enrolled_class_target,
            'staff_access': staff_access,
            'studio_url': studio_url,
            'is_cosmetic_price_enabled': settings.FEATURES.get('ENABLE_COSMETIC_DISPLAY_PRICE'),
            'course_price': course_price,
            'reg_then_add_to_cart_link': reg_then_add_to_cart_link,
            'invitation_only': invitation_only,
            # We do not want to display the internal courseware header, which is used when the course is found in the
            # context. This value is therefor explicitly set to render the appropriate header.
            'disable_courseware_header': True,
            'can_add_course_to_cart': can_add_course_to_cart,
            'cart_link': reverse('shoppingcart.views.show_cart'),
            'pre_requisite_courses': pre_requisite_courses,
            'course_image_urls': overview.image_urls,
            'meta_tags': meta_tags,
            'is_alquity': is_alquity,
            'social_sharing_urls': social_sharing_urls,
            'org_survey_status': user_org_survey_completion_status(request.user)
        }
        inject_coursetalk_keys_into_context(context, course_key)

        return render_to_response('courseware/course_about.html', context)
