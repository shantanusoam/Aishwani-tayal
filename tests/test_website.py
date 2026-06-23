from django.urls import reverse


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
