import pytest
import datetime
from django.urls import reverse

from website.models import Insight

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


def test_global_context_processor(client):
    """
    Test that the global context processor injects the correct site name and email.
    """
    url = reverse("website:home")
    response = client.get(url)
    assert "site_name" in response.context
    assert response.context["site_name"] == "Aishwani Tayal"
    assert "contact_email" in response.context
    assert response.context["contact_email"] == "contact@aishwanitayal.com"


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
