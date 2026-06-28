from .models import SocialLink


def global_context(request):
    """
    Exposes global context variables for website templates.
    """
    links = list(SocialLink.objects.filter(is_active=True).order_by("order", "id"))
    if not links:
        links = [
            SocialLink.objects.create(
                label="Linktree",
                url="https://linktr.ee/ca_ashwanitayal",
                icon_name="link",
                order=1,
                is_active=True,
            )
        ]

    return {
        "site_name": "Aishwani Tayal",
        "contact_email": "contact@aishwanitayal.com",
        "social_links": links,
    }
