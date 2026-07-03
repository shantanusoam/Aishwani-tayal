import pytest
from django.contrib.admin.sites import AdminSite
from tinymce.widgets import AdminTinyMCE

from website.admin import InsightAdmin
from website.models import Insight
from website.templatetags.richtext import richtext_excerpt_filter, richtext_filter

pytestmark = pytest.mark.django_db


def test_richtext_allows_safe_markup():
    html = '<p>Hello <strong>world</strong></p>'
    result = str(richtext_filter(html))
    assert "<strong>world</strong>" in result
    assert "<p>" in result


def test_richtext_converts_plain_text_linebreaks():
    value = "Line one\n\nLine two"
    result = str(richtext_filter(value))
    assert "Line one" in result
    assert "Line two" in result
    assert "<p>" in result


def test_richtext_strips_script_tags():
    value = '<p>Safe</p><script>alert("xss")</script>'
    result = str(richtext_filter(value))
    assert "Safe" in result
    assert "script" not in result.lower()


def test_richtext_strips_disallowed_attributes():
    value = '<p onerror="alert(1)">Text</p>'
    result = str(richtext_filter(value))
    assert "onerror" not in result
    assert "Text" in result


def test_richtext_excerpt_truncates_long_plain_text():
    value = " ".join(["word"] * 50)
    result = str(richtext_excerpt_filter(value, 10))
    assert result.endswith("…")
    assert result.count("word") == 10


def test_insight_admin_uses_tinymce_for_summary():
    admin = InsightAdmin(Insight, AdminSite())
    field = Insight._meta.get_field("summary")
    formfield = admin.formfield_for_dbfield(field, request=None)
    assert isinstance(formfield.widget, AdminTinyMCE)
