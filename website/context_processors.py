def global_context(request):
    """
    Exposes global context variables for website templates.
    """
    return {
        "site_name": "Aishwani Tayal",
        "contact_email": "contact@aishwanitayal.com",
    }
