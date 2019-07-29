def get_params_for_activation_email(request, registration, user):
    activation_link = '{protocol}://{site}/activate/{key}'.format(
        protocol='https' if request.is_secure() else 'http',
        site=safe_get_host(request),
        key=registration.activation_key
    )
    data = {
        "activation_link": activation_link,
        "user_email": user.email,
        'first_name': user.first_name,
    }

    return data
