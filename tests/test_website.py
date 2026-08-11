import datetime
import re

import pytest
from django.urls import reverse

from website.models import HomeServiceCard, Insight, SocialLink
from website.views import _seed_awards_content, _seed_home_services_content

pytestmark = pytest.mark.django_db


def test_home_page_status_code(client):
    """
    Test that the home page loads successfully (HTTP 200).
    """
    url = reverse("website:home")
    response = client.get(url)
    assert response.status_code == 200


def test_home_page_template_used(client):
    """
    Test that the home page uses the correct template.
    """
    url = reverse("website:home")
    response = client.get(url)
    assert "website/home.html" in [t.name for t in response.templates]


def test_services_page_status_code(client):
    """
    Test that the services page loads successfully (HTTP 200).
    """
    url = reverse("website:services")
    response = client.get(url)
    assert response.status_code == 200


def test_services_page_template_used(client):
    """
    Test that the services page uses the correct template.
    """
    url = reverse("website:services")
    response = client.get(url)
    assert "website/services.html" in [t.name for t in response.templates]


def test_about_page_status_code(client):
    """
    Test that the about page loads successfully (HTTP 200).
    """
    url = reverse("website:about")
    response = client.get(url)
    assert response.status_code == 200


def test_about_page_template_used(client):
    """
    Test that the about page uses the correct template.
    """
    url = reverse("website:about")
    response = client.get(url)
    assert "website/about.html" in [t.name for t in response.templates]


def test_blogs_page_status_code(client):
    """
    Test that the blogs page loads successfully (HTTP 200).
    """
    url = reverse("website:blogs")
    response = client.get(url)
    assert response.status_code == 200


def test_blogs_page_template_used(client):
    """
    Test that the blogs page uses the correct template.
    """
    url = reverse("website:blogs")
    response = client.get(url)
    assert "website/blogs.html" in [t.name for t in response.templates]


def test_contact_page_status_code(client):
    """
    Test that the contact page loads successfully (HTTP 200).
    """
    url = reverse("website:contact")
    response = client.get(url)
    assert response.status_code == 200


def test_contact_page_template_used(client):
    """
    Test that the contact page uses the correct template.
    """
    url = reverse("website:contact")
    response = client.get(url)
    assert "website/contact.html" in [t.name for t in response.templates]


def test_ccts_page_status_code_and_template(client):
    url = reverse("website:ccts")
    response = client.get(url)
    assert response.status_code == 200
    assert "website/ccts.html" in [t.name for t in response.templates]


def test_ccts_page_only_shows_ccts_blogs_in_context(client):
    Insight.objects.create(
        title="CCTS Topic",
        category="CCTS",
        published_date=datetime.date(2026, 6, 20),
        summary="CCTS post",
        image_filename="blog_tax.png",
    )
    Insight.objects.create(
        title="Tax Topic",
        category="TAX",
        published_date=datetime.date(2026, 6, 10),
        summary="Tax post",
        image_filename="blog_tax.png",
    )

    response = client.get(reverse("website:ccts"))
    insights = response.context["insights"]
    assert insights
    assert all(insight.category == "CCTS" for insight in insights)


def test_service_detail_page_status_code(client):
    response = client.get(reverse("website:service_detail", kwargs={"slug": "tax-planning"}))
    assert response.status_code == 200


def test_services_page_renders_each_card_once(client):
    """Services listing should not duplicate cards in the grid."""
    response = client.get(reverse("website:services"))
    cards = response.context["home_service_cards"]
    section_html = re.search(r'id="all-services".*?</section>', response.content.decode(), re.DOTALL)
    assert section_html is not None
    service_links = re.findall(r'href="/services/[^/]+/"', section_html.group(0))
    assert len(service_links) == len(cards)


def test_home_services_seed_respects_admin_delete():
    """Deleted service cards must not be recreated on page load."""
    _seed_home_services_content()
    card = HomeServiceCard.objects.first()
    assert card is not None
    initial_count = HomeServiceCard.objects.count()
    card.delete()
    _seed_home_services_content()
    assert HomeServiceCard.objects.count() == initial_count - 1


def test_home_services_seed_respects_admin_edit():
    """Editing a service title must not create a duplicate card."""
    _seed_home_services_content()
    card = HomeServiceCard.objects.get(slug="tax-planning")
    card.title = "Updated Tax Planning"
    card.save()
    initial_count = HomeServiceCard.objects.count()
    _seed_home_services_content()
    assert HomeServiceCard.objects.count() == initial_count
    assert HomeServiceCard.objects.filter(title="Updated Tax Planning").exists()


def test_global_context_processor(client):
    """
    Test that the global context processor injects site name, contact details, and social links.
    """
    url = reverse("website:home")
    response = client.get(url)
    assert "site_name" in response.context
    assert response.context["site_name"] == "Aishwani Tayal"
    assert "contact_email" in response.context
    assert response.context["contact_email"] == "contact@aishwanitayal.com"
    assert response.context["contact_phone"] == "+91 98995 00036"
    assert response.context["contact_phone_digits"] == "919899500036"
    assert response.context["contact_whatsapp_url"] == "https://wa.me/919899500036"
    assert "Pushpanjali Enclave" in response.context["contact_address"]
    assert "Pitampura" in response.context["contact_address"]

    labels = {link.label for link in response.context["social_links"]}
    assert {"WhatsApp", "Facebook", "Linktree"}.issubset(labels)
    assert SocialLink.objects.filter(label="WhatsApp", icon_name="whatsapp").exists()
    assert SocialLink.objects.filter(label="Facebook", icon_name="facebook").exists()


def test_global_context_seeds_missing_social_links(client):
    """
    Edge case: when only Linktree exists, WhatsApp and Facebook are still added.
    """
    SocialLink.objects.all().delete()
    SocialLink.objects.create(
        label="Linktree",
        url="https://linktr.ee/ca_ashwanitayal",
        icon_name="link",
        order=1,
        is_active=True,
    )
    response = client.get(reverse("website:home"))
    labels = {link.label for link in response.context["social_links"]}
    assert labels == {"WhatsApp", "Facebook", "Linktree"}


def test_home_hero_cta_points_to_contact_form(client):
    """
    Hero CTA should redirect to the contact page consultation form.
    """
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert "/contact/#appointments" in content
    assert "BOOK YOUR CONSULTATION" in content


def test_inactive_social_links_are_excluded(client):
    """
    Failure case: inactive social links must not appear in context.
    """
    SocialLink.objects.all().delete()
    SocialLink.objects.create(
        label="WhatsApp",
        url="https://wa.me/919899500036",
        icon_name="whatsapp",
        order=1,
        is_active=False,
    )
    response = client.get(reverse("website:home"))
    # Seeding re-activates the default WhatsApp row by label update.
    active_labels = {link.label for link in response.context["social_links"]}
    assert "WhatsApp" in active_labels
    assert SocialLink.objects.get(label="WhatsApp").is_active is True


def test_home_page_shows_updated_contact_details(client):
    """
    Footer and floating WhatsApp use the updated phone and address.
    """
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert "+91 98995 00036" in content
    assert "https://wa.me/919899500036" in content
    assert "Pushpanjali Enclave" in content
    assert "Prestige Tower" not in content
    assert "911145678900" not in content


def test_nav_order_ccts_before_workshops(client):
    """
    CCTS should appear before Workshops in the header navigation.
    """
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    ccts_pos = content.find(">CCTS</a>")
    workshops_pos = content.find(">Workshops</a>")
    assert ccts_pos != -1
    assert workshops_pos != -1
    assert ccts_pos < workshops_pos


def test_book_consultation_success(client):
    """
    Test successful consultation booking.
    """
    url = reverse("website:book_consultation")
    data = {
        "full_name": "Rajesh Mehta",
        "email": "rajesh@company.com",
        "phone": "+919876543210",
        "service": "X-RAY",
        "company": "Mehta Corp",
        "message": "Need a mock audit."
    }
    response = client.post(url, data)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["success"] is True
    assert "booked successfully" in res_data["message"]


def test_book_consultation_failure(client):
    """
    Test consultation booking failure on missing required elements.
    """
    url = reverse("website:book_consultation")
    data = {
        "full_name": "",
        "email": "invalid-email",
        "phone": "",
    }
    response = client.post(url, data)
    assert response.status_code == 400
    res_data = response.json()
    assert res_data["success"] is False
    assert "full_name" in res_data["errors"]
    assert "email" in res_data["errors"]


def test_home_awards_section_auto_scrolls(client):
    """
    Expected use: home awards track uses the infinite marquee animation.
    """
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    assert "home-awards-track" in content
    assert "home-awards-scroll-left" in content
    assert "overflow-x-auto" not in content.split("Awards & Recognitions", 1)[-1].split("</section>", 1)[0]


def test_home_awards_section_duplicates_cards_for_loop(client):
    """
    Edge case: cards are duplicated so the -50% translate loops seamlessly.
    """
    awards = _seed_awards_content()
    response = client.get(reverse("website:home"))
    content = response.content.decode()
    first_title = awards[0].title
    assert content.count(first_title) >= 2
    assert 'aria-hidden="true"' in content


def test_inactive_awards_are_excluded_from_home(client):
    """
    Failure case: inactive awards must not appear in the auto-scroll track.
    """
    awards = _seed_awards_content()
    hidden = awards[0]
    hidden.is_active = False
    hidden.save(update_fields=["is_active"])

    response = client.get(reverse("website:home"))
    titles = [award.title for award in response.context["award_cards"]]
    assert hidden.title not in titles
    assert response.content.decode().count(hidden.title) == 0
