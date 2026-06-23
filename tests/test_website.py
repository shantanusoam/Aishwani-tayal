import pytest
from django.urls import reverse

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

