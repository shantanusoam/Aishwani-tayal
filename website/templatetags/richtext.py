import re

import bleach
from django import template
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "u",
    "ul",
    "ol",
    "li",
    "a",
    "h2",
    "h3",
    "h4",
    "blockquote",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
}
HTML_TAG_RE = re.compile(r"<[^>]+>")


def _prepare_plain_text(value: str) -> str:
    if not HTML_TAG_RE.search(value):
        return linebreaks(value, autoescape=True)
    return value


def _sanitize_html(value: str) -> str:
    cleaned = bleach.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
    )
    return bleach.linkify(
        cleaned,
        callbacks=[bleach.callbacks.nofollow, bleach.callbacks.target_blank],
    )


@register.filter(name="richtext")
def richtext_filter(value):
    if not value:
        return ""
    prepared = _prepare_plain_text(str(value))
    return mark_safe(_sanitize_html(prepared))


@register.filter(name="richtext_excerpt")
def richtext_excerpt_filter(value, word_count=30):
    if not value:
        return ""
    prepared = _prepare_plain_text(str(value))
    sanitized = _sanitize_html(prepared)
    from django.utils.html import strip_tags

    plain = strip_tags(sanitized)
    words = plain.split()
    if len(words) <= int(word_count):
        return mark_safe(sanitized)
    excerpt = " ".join(words[: int(word_count)]) + "…"
    return mark_safe(excerpt)
