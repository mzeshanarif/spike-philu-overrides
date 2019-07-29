def send_account_activation_email(request, registration, user):
    activation_link = '{protocol}://{site}/activate/{key}'.format(
            protocol='https' if request.is_secure() else 'http',
            site=safe_get_host(request),
            key=registration.activation_key
        )

    context = {
        'first_name': user.first_name,
        'activation_link': activation_link,
    }
    MandrillClient().send_mail(MandrillClient.USER_ACCOUNT_ACTIVATION_TEMPLATE, user.email, context)
