# /edx-platform/common/djangoapps/student/views.py

def _do_create_account(form, custom_form=None):
    """
    Given cleaned post variables, create the User and UserProfile objects, as well as the
    registration for this user.

    Returns a tuple (User, UserProfile, Registration).

    Note: this function is also used for creating test users.
    """
    errors = {}
    errors.update(form.errors)
    if custom_form:
        errors.update(custom_form.errors)

    if errors:
        raise ValidationError(errors)

    user = User(
        username=form.cleaned_data["username"],
        email=form.cleaned_data["email"],
        is_active=False
    )
    user.set_password(form.cleaned_data["password"])
    registration = Registration()

    # TODO: Rearrange so that if part of the process fails, the whole process fails.
    # Right now, we can have e.g. no registration e-mail sent out and a zombie account
    try:
        with transaction.atomic():
            user.save()
            if custom_form:
                custom_model = custom_form.save(user=user, commit=True)

    except IntegrityError:
        # Figure out the cause of the integrity error
        if len(User.objects.filter(username=user.username)) > 0:
            raise AccountValidationError(
                _("An account with the Public Username '{username}' already exists.").format(username=user.username),
                field="username"
            )
        elif len(User.objects.filter(email=user.email)) > 0:
            raise AccountValidationError(
                _("An account with the Email '{email}' already exists.").format(email=user.email),
                field="email"
            )
        else:
            raise

    # add this account creation to password history
    # NOTE, this will be a NOP unless the feature has been turned on in configuration
    password_history_entry = PasswordHistory()
    password_history_entry.create(user)

    registration.register(user)

    profile_fields = [
        "name", "level_of_education", "gender", "mailing_address", "city", "country", "goals",
        "year_of_birth"
    ]
    profile = UserProfile(
        user=user,
        **{key: form.cleaned_data.get(key) for key in profile_fields}
    )
    extended_profile = form.cleaned_extended_profile
    if extended_profile:
        profile.meta = json.dumps(extended_profile)
    try:
        profile.save()
    except Exception:  # pylint: disable=broad-except
        log.exception("UserProfile creation failed for user {id}.".format(id=user.id))
        raise

    return (user, profile, registration)
