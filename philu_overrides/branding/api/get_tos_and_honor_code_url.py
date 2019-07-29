# edx-platform/lms/djangoapps/branding/api.py

def get_tos_and_honor_code_url():
    """
    Lookup and return terms of services page url
    """
    return get_url("TOS_AND_HONOR")
