    def save_user_utm_info(self, user):

        """
        :param user:
            user for which utm params are being saved + request to get all utm related params
        :return:
        """
        def extract_param_value(request, param_name):
            utm_value = request.POST.get(param_name, None)

            if not utm_value and param_name in request.session:
                utm_value = request.session[param_name]
                del request.session[param_name]

            return utm_value

        try:
            utm_source = extract_param_value(self.request, "utm_source")
            utm_medium = extract_param_value(self.request, "utm_medium")
            utm_campaign = extract_param_value(self.request, "utm_campaign")
            utm_content = extract_param_value(self.request, "utm_content")
            utm_term = extract_param_value(self.request, "utm_term")

            from openedx.features.user_leads.models import UserLeads
            UserLeads.objects.create(
                utm_source=utm_source,
                utm_medium=utm_medium,
                utm_campaign=utm_campaign,
                utm_content=utm_content,
                utm_term=utm_term,
                user=user
            )
        except Exception as ex:
            log.error("There is some error saving UTM {}".format(str(ex)))
            pass
