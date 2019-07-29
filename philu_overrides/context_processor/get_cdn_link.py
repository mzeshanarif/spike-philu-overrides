def get_cdn_link(request):
    """
    return CDN url link to templates
    :return:
    """
    return {"cdn_link": settings.CDN_LINK}
