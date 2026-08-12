from .models import SocialLink

CONTACT_PHONE = "+91 98995 00036"
CONTACT_PHONE_DIGITS = "919899500036"
CONTACT_WHATSAPP_URL = f"https://wa.me/{CONTACT_PHONE_DIGITS}"
CONTACT_ADDRESS = (
    "3rd Floor (4th Floor By Lift), Pushpanjali Enclave, Behind Bus Stand, "
    "B-20, Outer Ring Rd, Pitampura, Delhi, 110034"
)
CONTACT_TIMING = "Mon-Fri: 8:30 AM - 5:30 PM"
LINKTREE_URL = "https://linktr.ee/ca_ashwanitayal"

# Reason: ensure brand icons exist even when only Linktree was seeded earlier.
DEFAULT_SOCIAL_LINKS = (
    {"label": "WhatsApp", "url": CONTACT_WHATSAPP_URL, "icon_name": "whatsapp", "order": 1},
    {"label": "Facebook", "url": LINKTREE_URL, "icon_name": "facebook", "order": 2},
    {"label": "Linktree", "url": LINKTREE_URL, "icon_name": "link", "order": 3},
)


def _ensure_social_links():
    """Create missing default social links by label; return active links."""
    for defaults in DEFAULT_SOCIAL_LINKS:
        SocialLink.objects.get_or_create(
            label=defaults["label"],
            defaults={
                "url": defaults["url"],
                "icon_name": defaults["icon_name"],
                "order": defaults["order"],
                "is_active": True,
            },
        )

    # Keep WhatsApp URL in sync with the current phone number.
    SocialLink.objects.filter(label="WhatsApp").update(
        url=CONTACT_WHATSAPP_URL,
        icon_name="whatsapp",
        is_active=True,
    )

    return list(SocialLink.objects.filter(is_active=True).order_by("order", "id"))


def global_context(request):
    """
    Exposes global context variables for website templates.
    """
    links = _ensure_social_links()

    return {
        "site_name": "Aishwani Tayal",
        "contact_email": "contact@aishwanitayal.com",
        "contact_phone": CONTACT_PHONE,
        "contact_phone_digits": CONTACT_PHONE_DIGITS,
        "contact_whatsapp_url": CONTACT_WHATSAPP_URL,
        "contact_address": CONTACT_ADDRESS,
        "contact_timing": CONTACT_TIMING,
        "social_links": links,
    }
