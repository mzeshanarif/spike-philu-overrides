def save_user_partner_network_consent(user, _data):
    if _data:
        organization = user.extended_profile.organization
        consents = json.loads(_data)
        for _c in consents:
            organization_partner = organization.organization_partners.filter(
                partner=_c['code'], end_date=ORG_PARTNERSHIP_END_DATE_PLACEHOLDER
            ).first()
            if organization_partner:
                GranteeOptIn.objects.create(
                    agreed=_c['consent'] == 'true',
                    organization_partner=organization_partner,
                    user=user
                )
