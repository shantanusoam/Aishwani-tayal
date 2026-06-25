from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.conf import settings
from django.urls import reverse
import datetime
from pathlib import Path

from .models import (
    Insight,
    HomeServiceSection,
    HomeServiceCard,
    AboutHeroSection,
    AboutHeroPanel,
)
from .forms import ConsultationForm


def _seed_home_services_content():
    section = HomeServiceSection.objects.order_by("id").first()
    if section is None:
        section = HomeServiceSection.objects.create(
            label="What We Offer",
            title="Expertise That Drives Real Results",
            description="Comprehensive financial solutions designed to support every stage of your business journey.",
            cta_text="View All Services",
            cta_url=reverse("website:services"),
        )

    if section.cards.exists():
        return section

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "title": "Tax Planning",
            "summary": "Comprehensive income tax planning and optimisation strategies for individuals, HUFs, and corporates.",
            "filename": "service_tax.png",
            "badge_one": "Direct Tax",
            "badge_two": "Optimisation",
            "order": 1,
        },
        {
            "title": "Audit & Assurance",
            "summary": "Statutory, internal, and forensic audits with meticulous attention to detail and regulatory compliance.",
            "filename": "service_audit.png",
            "badge_one": "Statutory",
            "badge_two": "Forensic",
            "order": 2,
        },
        {
            "title": "Business Advisory (Design Your Business)",
            "summary": "Strategic guidance on business restructuring, mergers, acquisitions, and sustainable growth planning.",
            "filename": "service_biz.png",
            "badge_one": "Strategy",
            "badge_two": "M&A",
            "order": 3,
        },
        {
            "title": "GST Consultancy",
            "summary": "Complete GST advisory, registration, return filing, and resolution of complex GST disputes.",
            "filename": "service_gst.png",
            "badge_one": "Indirect Tax",
            "badge_two": "Compliance",
            "order": 4,
        },
        {
            "title": "Corporate Compliance",
            "summary": "ROC filings, company law compliance, FEMA, and secretarial services for corporates of all sizes.",
            "filename": "service_compliance.png",
            "badge_one": "Company Law",
            "badge_two": "FEMA",
            "order": 5,
        },
        {
            "title": "Financial Strategy",
            "summary": "CFO advisory services, fundraising support, and long-term financial structuring for business growth.",
            "filename": "service_strategy.png",
            "badge_one": "CFO Advisory",
            "badge_two": "Fundraising",
            "order": 6,
        },
    ]

    for card_data in seed_cards:
        card = HomeServiceCard(section=section)
        card.title = card_data["title"]
        card.summary = card_data["summary"]
        card.image_alt = card_data["title"]
        card.badge_one = card_data["badge_one"]
        card.badge_two = card_data["badge_two"]
        card.link_url = reverse("website:services")
        card.order = card_data["order"]

        image_path = static_dir / card_data["filename"]
        if image_path.exists():
            card.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        card.save()

    return section


def _get_award_cards():
    return [
        {
            "year": "2024",
            "title": "Best CA Advisor of the Year",
            "source": "ICAI National Conference",
            "image": "images/award_ceremony.png",
            "image_alt": "Best CA Advisor of the Year award",
            "featured": True,
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "National Business Council",
            "image": "images/cert_gst_advisor.png",
            "image_alt": "Excellence in GST Advisory award",
            "featured": False,
        },
    ]


def _get_about_award_cards():
    return [
        {
            "year": "2024",
            "title": "Best CA Advisor of the Year",
            "source": "ICAI National Conference",
            "image": "images/cert_ca_advisor.png",
            "image_alt": "Certificate for Best CA Advisor of the Year",
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "Federation of Indian Chambers",
            "image": "images/cert_gst_advisor.png",
            "image_alt": "Certificate for Excellence in GST Advisory",
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "image": "images/cert_corp_recog_1.png",
            "image_alt": "Corporate Recognition Award certificate",
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "image": "images/cert_corp_recog_2.png",
            "image_alt": "Corporate Recognition Award certificate",
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "Federation of Indian Chambers",
            "image": "images/cert_gst_advisor.png",
            "image_alt": "Certificate for Excellence in GST Advisory",
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "image": "images/cert_membership.png",
            "image_alt": "Corporate Recognition Award certificate",
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "image": "images/cert_diploma_trade.png",
            "image_alt": "Corporate Recognition Award certificate",
        },
    ]


def _seed_about_hero_content():
    section = AboutHeroSection.objects.order_by("id").first()
    if section is None:
        section = AboutHeroSection.objects.create(
            pretitle="KNOW ME BETTER",
            title_line_one="Experience.",
            title_line_two="Expertise.",
            title_highlight="Impact.",
            description=(
                "A journey of trust, learning and leadership that has empowered businesses, "
                "inspired professionals and created lasting impact."
            ),
            image_filename="about_hero_portrait.png",
            image_alt="CA Ashwani Tayal",
        )

    if section.panels.exists():
        return section

    panel_data = [
        {
            "number": "01",
            "title": "Author",
            "subtitle": "Thought Leader",
            "icon_name": "book-open",
            "tone": "navy",
            "order": 1,
        },
        {
            "number": "02",
            "title": "Motivational Speaker",
            "subtitle": "Inspiring Growth",
            "icon_name": "mic",
            "tone": "blue",
            "order": 2,
        },
        {
            "number": "03",
            "title": "ICAI Faculty",
            "subtitle": "Direct Tax / Indirect Tax / International Tax",
            "icon_name": "graduation-cap",
            "tone": "midblue",
            "order": 3,
        },
        {
            "number": "04",
            "title": "Practicing CA",
            "subtitle": "for 21 Years",
            "icon_name": "briefcase",
            "tone": "gold",
            "order": 4,
        },
        {
            "number": "05",
            "title": "Business Mentor",
            "subtitle": "500+ Entrepreneurs",
            "icon_name": "users",
            "tone": "lightgold",
            "order": 5,
        },
    ]

    for panel_info in panel_data:
        AboutHeroPanel.objects.create(section=section, **panel_info)

    return section


def home(request):
    """
    Renders the homepage with insights and consultation forms.
    """
    insights = list(Insight.objects.all().order_by("-published_date"))

    # Seed insights data if empty (dynamic database setup)
    if not insights:
        seed_data = [
            {
                "title": "How to Optimise Your Tax Liability in FY 2025–26",
                "category": "TAX",
                "published_date": datetime.date(2026, 6, 12),
                "summary": "A step-by-step breakdown of the most effective strategies to legally minimize your personal and corporate taxes under the latest Union Budget provisions.",
                "image_filename": "blog_tax.png",
            },
            {
                "title": "GST Input Tax Credit: Common Mistakes & How to Avoid Them",
                "category": "GST",
                "published_date": datetime.date(2026, 5, 28),
                "summary": "ITC mismatches are among the top reasons for audit notices. Learn our bulletproof process to audit and reconcile purchase logs with GSTR-2B.",
                "image_filename": "blog_gst.png",
            },
            {
                "title": "Structuring Your Business for Long-term Growth",
                "category": "BIZ",
                "published_date": datetime.date(2026, 5, 10),
                "summary": "From entity selection to corporate restructuring, discover how seasoned structures protect your wealth and facilitate easy fundraises.",
                "image_filename": "blog_growth.png",
            },
        ]
        for data in seed_data:
            insight = Insight.objects.create(
                title=data["title"],
                category=data["category"],
                published_date=data["published_date"],
                summary=data["summary"],
                image_filename=data["image_filename"],
            )
            insights.append(insight)

    form = ConsultationForm()
    home_service_section = _seed_home_services_content()
    home_service_cards = list(home_service_section.cards.all().order_by("order", "id"))
    award_cards = _get_award_cards()

    return render(
        request,
        "website/home.html",
        {
            "insights": insights,
            "form": form,
            "home_service_section": home_service_section,
            "home_service_cards": home_service_cards,
            "award_cards": award_cards,
        },
    )


def services(request):
    """
    Renders the Carbon Credit Trading Scheme (CCTS) & comprehensive services page.
    """
    insights = Insight.objects.all().order_by("-published_date")[:3]
    form = ConsultationForm()
    home_service_section = _seed_home_services_content()
    home_service_cards = list(home_service_section.cards.all().order_by("order", "id"))
    return render(
        request,
        "website/services.html",
        {
            "insights": insights,
            "form": form,
            "home_service_section": home_service_section,
            "home_service_cards": home_service_cards,
            "blogs_url": reverse("website:blogs"),
        },
    )


def about(request):
    """
    Renders the detailed CA Ashwani Tayal biography, certifications, & values page.
    """
    form = ConsultationForm()
    about_hero_section = _seed_about_hero_content()
    about_hero_panels = list(about_hero_section.panels.all().order_by("order", "id"))
    about_award_cards = _get_about_award_cards()
    about_award_cards_top = about_award_cards[:4]
    about_award_cards_bottom = about_award_cards[4:]
    return render(
        request,
        "website/about.html",
        {
            "form": form,
            "about_award_cards_top": about_award_cards_top,
            "about_award_cards_bottom": about_award_cards_bottom,
            "about_hero_section": about_hero_section,
            "about_hero_panels": about_hero_panels,
        },
    )


def blogs(request):
    """
    Renders the comprehensive blogs & insights page.
    """
    insights = list(Insight.objects.all().order_by("-published_date"))

    # Seed insights data if empty (dynamic database setup)
    if not insights:
        seed_data = [
            {
                "title": "How to Optimise Your Tax Liability in FY 2025–26",
                "category": "TAX",
                "published_date": datetime.date(2026, 6, 12),
                "summary": "A step-by-step breakdown of the most effective strategies to legally minimize your personal and corporate taxes under the latest Union Budget provisions.",
                "image_filename": "blog_tax.png",
            },
            {
                "title": "GST Input Tax Credit: Common Mistakes & How to Avoid Them",
                "category": "GST",
                "published_date": datetime.date(2026, 5, 28),
                "summary": "ITC mismatches are among the top reasons for audit notices. Learn our bulletproof process to audit and reconcile purchase logs with GSTR-2B.",
                "image_filename": "blog_gst.png",
            },
            {
                "title": "Structuring Your Business for Long-term Growth",
                "category": "BIZ",
                "published_date": datetime.date(2026, 5, 10),
                "summary": "From entity selection to corporate restructuring, discover how seasoned structures protect your wealth and facilitate easy fundraises.",
                "image_filename": "blog_growth.png",
            },
        ]
        for data in seed_data:
            insight = Insight.objects.create(
                title=data["title"],
                category=data["category"],
                published_date=data["published_date"],
                summary=data["summary"],
                image_filename=data["image_filename"],
            )
            insights.append(insight)

    form = ConsultationForm()
    return render(request, "website/blogs.html", {"insights": insights, "form": form})


@require_POST
def book_consultation(request):
    """
    Saves consultation requests via AJAX/JSON submission.
    """
    form = ConsultationForm(request.POST)
    if form.is_valid():
        consultation = form.save()
        return JsonResponse(
            {
                "success": True,
                "message": "Thank you, Rajesh Mehta! Your consultation has been booked successfully. CA Ashwani Tayal's team will touch base in 2 hours.",
                "request_id": consultation.id,
            }
        )
    else:
        errors = {field: errors[0] for field, errors in form.errors.items()}
        return JsonResponse({"success": False, "errors": errors}, status=400)
