    def _apply_third_party_auth_overrides(self, request, form_desc):
        """Modify the registration form if the user has authenticated with a third-party provider.
        If a user has successfully authenticated with a third-party provider,
        but does not yet have an account with PhilU, we want to fill in
        the registration form with any info that we get from the
        provider.
        Arguments:
            request (HttpRequest): The request for the registration form, used
                to determine if the user has successfully authenticated
                with a third-party provider.
            form_desc (FormDescription): The registration form description
        """
        if third_party_auth.is_enabled():
            running_pipeline = third_party_auth.pipeline.get(request)
            if running_pipeline:
                current_provider = third_party_auth.provider.Registry.get_from_pipeline(running_pipeline)

                if current_provider:
                    # Override username / email / full name
                    field_overrides = get_register_form_data_override(
                        running_pipeline.get('kwargs')
                    )

                    for field_name in self.THIRD_PARTY_OVERRIDE_FIELDS:
                        if field_name in field_overrides:

                            if field_name == 'username':
                                try:
                                    validate_slug(field_overrides[field_name])
                                except ValidationError:
                                    continue

                            form_desc.override_field_properties(
                                field_name, default=field_overrides[field_name]
                            )
