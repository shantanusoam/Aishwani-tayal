from django.shortcuts import get_object_or_404, render
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
    HomeFeaturedServiceSection,
    HomeFeaturedServiceCard,
    AboutHeroSection,
    AboutHeroPanel,
    AboutIntroSection,
    AboutIntroFeature,
    AboutCertification,
    TestimonialVideo,
    Award,
    MomentMilestone,
    FAQ,
    CCTSServiceSection,
    CCTSServiceCard,
    ServiceDetailHeroSlide,
)
from .forms import ConsultationForm


def _ensure_default_insights():
    insights = list(Insight.objects.all().order_by("-published_date"))
    if insights:
        return insights

    seed_data = [
        {
            "title": "CCTS Compliance: What CFOs Must Prepare This Quarter",
            "category": "CCTS",
            "published_date": datetime.date(2026, 6, 20),
            "summary": "A practical quarterly checklist for carbon accounting, disclosures, and governance under India's CCTS.",
            "image_filename": "blog_growth.png",
        },
        {
            "title": "Carbon Credit Accounting and Tax Treatment in India",
            "category": "CCTS",
            "published_date": datetime.date(2026, 6, 15),
            "summary": "How to classify, value, and report carbon credits with a defensible tax and audit trail.",
            "image_filename": "blog_gst.png",
        },
        {
            "title": "Could Your Company Face CCTS Penalties?",
            "category": "CCTS",
            "published_date": datetime.date(2026, 6, 8),
            "summary": "Understand enforcement exposure, documentation obligations, and board-level accountability under CCTS.",
            "image_filename": "blog_tax.png",
        },
        {
            "title": "How to Optimise Your Tax Liability in FY 2025–26",
            "category": "TAX",
            "published_date": datetime.date(2026, 6, 12),
            "summary": "A step-by-step breakdown of strategies to legally minimize personal and corporate taxes.",
            "image_filename": "blog_tax.png",
        },
        {
            "title": "GST Input Tax Credit: Common Mistakes & How to Avoid Them",
            "category": "GST",
            "published_date": datetime.date(2026, 5, 28),
            "summary": "A practical process to reconcile purchase records with GSTR-2B and reduce notice risk.",
            "image_filename": "blog_gst.png",
        },
        {
            "title": "Structuring Your Business for Long-term Growth",
            "category": "BIZ",
            "published_date": datetime.date(2026, 5, 10),
            "summary": "Entity, compliance, and planning structures that support better governance and fundraising.",
            "image_filename": "blog_growth.png",
        },
    ]
    created = [Insight.objects.create(**data) for data in seed_data]
    return list(sorted(created, key=lambda item: item.published_date, reverse=True))


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

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "title": "Tax Planning",
            "slug": "tax-planning",
            "summary": "Comprehensive income tax planning and optimisation strategies for individuals, HUFs, and corporates.",
            "filename": "service_tax.png",
            "badge_one": "Direct Tax",
            "badge_two": "Optimisation",
            "detail_kicker": "Direct Tax Advisory",
            "detail_heading": "Tax Planning That Protects Cash Flow",
            "detail_intro": "Income-tax planning for individuals, HUFs, business owners, and companies with a focus on compliant savings and audit-ready documentation.",
            "detail_body": "We review income streams, entity structure, deductions, investments, and compliance calendars to build a clear tax strategy before deadlines become pressure points.",
            "detail_points": "Personal and corporate tax optimisation\nAdvance tax and TDS planning\nCapital gains and transaction structuring\nAssessment and notice response support",
            "order": 1,
        },
        {
            "title": "Audit & Assurance",
            "slug": "audit-assurance",
            "summary": "Statutory, internal, and forensic audits with meticulous attention to detail and regulatory compliance.",
            "filename": "service_audit.png",
            "badge_one": "Statutory",
            "badge_two": "Forensic",
            "detail_kicker": "Audit Readiness",
            "detail_heading": "Assurance Built On Evidence",
            "detail_intro": "Statutory, internal, and forensic audit support for businesses that need reliable books, strong controls, and confidence in reporting.",
            "detail_body": "Our audit approach combines transaction-level review with practical control recommendations so leadership receives compliance coverage and decision-useful insights.",
            "detail_points": "Statutory and tax audit coordination\nInternal control review\nForensic and transaction checks\nManagement reporting and remediation plans",
            "order": 2,
        },
        {
            "title": "Business Advisory (Design Your Business)",
            "slug": "business-advisory",
            "summary": "Strategic guidance on business restructuring, mergers, acquisitions, and sustainable growth planning.",
            "filename": "service_biz.png",
            "badge_one": "Strategy",
            "badge_two": "M&A",
            "detail_kicker": "Business Structuring",
            "detail_heading": "Design Your Business For Scale",
            "detail_intro": "Strategic advisory for owners navigating growth, restructuring, acquisitions, succession, or sharper operating discipline.",
            "detail_body": "We translate business goals into entity structures, governance routines, financial controls, and measurable action plans.",
            "detail_points": "Entity and ownership structuring\nMergers, acquisitions, and restructuring support\nBusiness model and process review\nGrowth planning with financial guardrails",
            "order": 3,
        },
        {
            "title": "GST Consultancy",
            "slug": "gst-consultancy",
            "summary": "Complete GST advisory, registration, return filing, and resolution of complex GST disputes.",
            "filename": "service_gst.png",
            "badge_one": "Indirect Tax",
            "badge_two": "Compliance",
            "detail_kicker": "Indirect Tax",
            "detail_heading": "GST Clarity From Filing To Disputes",
            "detail_intro": "End-to-end GST advisory for registration, returns, input tax credit review, reconciliations, and complex dispute resolution.",
            "detail_body": "We identify leakage, mismatch exposure, documentation gaps, and compliance risks before they become notices or blocked credits.",
            "detail_points": "GST registration and return review\nInput tax credit reconciliation\nE-way bill and invoicing controls\nDepartment notice and dispute support",
            "order": 4,
        },
        {
            "title": "Corporate Compliance",
            "slug": "corporate-compliance",
            "summary": "ROC filings, company law compliance, FEMA, and secretarial services for corporates of all sizes.",
            "filename": "service_compliance.png",
            "badge_one": "Company Law",
            "badge_two": "FEMA",
            "detail_kicker": "Governance & ROC",
            "detail_heading": "Corporate Compliance Without Last-Minute Risk",
            "detail_intro": "Company law, ROC, FEMA, and secretarial compliance support for startups, SMEs, and growing corporates.",
            "detail_body": "We maintain a proactive compliance rhythm so statutory filings, board records, and governance documents stay current and investor-ready.",
            "detail_points": "ROC forms and annual filings\nBoard and shareholder documentation\nFEMA and regulatory coordination\nCompliance calendar and governance reviews",
            "order": 5,
        },
        {
            "title": "Financial Strategy",
            "slug": "financial-strategy",
            "summary": "CFO advisory services, fundraising support, and long-term financial structuring for business growth.",
            "filename": "service_strategy.png",
            "badge_one": "CFO Advisory",
            "badge_two": "Fundraising",
            "detail_kicker": "CFO Advisory",
            "detail_heading": "Financial Strategy For Better Decisions",
            "detail_intro": "CFO advisory, fundraising support, forecasting, and long-term financial structuring for businesses preparing for their next stage.",
            "detail_body": "We help leaders understand runway, margins, capital requirements, funding options, and board-level reporting so finance becomes a growth engine.",
            "detail_points": "Virtual CFO and MIS setup\nForecasting and cash-flow planning\nFundraising and lender readiness\nPricing, margin, and unit-economics review",
            "order": 6,
        },
    ]

    for card_data in seed_cards:
        card, created = HomeServiceCard.objects.get_or_create(
            section=section,
            title=card_data["title"],
            defaults={"summary": card_data["summary"]},
        )
        card.title = card_data["title"]
        card.slug = card_data["slug"]
        card.summary = card_data["summary"]
        card.image_alt = card_data["title"]
        card.badge_one = card_data["badge_one"]
        card.badge_two = card_data["badge_two"]
        card.link_url = reverse("website:service_detail", kwargs={"slug": card_data["slug"]})
        card.detail_kicker = card_data["detail_kicker"]
        card.detail_heading = card_data["detail_heading"]
        card.detail_intro = card_data["detail_intro"]
        card.detail_body = card_data["detail_body"]
        card.detail_points = card_data["detail_points"]
        card.order = card_data["order"]

        image_path = static_dir / card_data["filename"]
        if created and image_path.exists():
            card.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        card.save()

    return section


def _seed_home_featured_services():
    section = HomeFeaturedServiceSection.objects.order_by("id").first()
    if section is None:
        section = HomeFeaturedServiceSection.objects.create(title="Home Featured Services")

    existing_cards = list(section.cards.order_by("order", "id"))
    if existing_cards:
        return [card for card in existing_cards if card.is_active]

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "title": "X-RAY Framework",
            "subtitle": "Investigation & Diagnosis",
            "filename": "figma_xray_framework.png",
            "cta_url": f'{reverse("website:services")}#expertise',
            "order": 1,
        },
        {
            "title": "CCTS",
            "subtitle": "Measure & Monetize",
            "filename": "figma_ccts_card.png",
            "cta_url": reverse("website:ccts"),
            "order": 2,
        },
        {
            "title": "Virtual CFO",
            "subtitle": "Review & Forecast",
            "filename": "figma_virtual_cfo.png",
            "cta_url": f'{reverse("website:services")}#expertise',
            "order": 3,
        },
    ]

    cards = []
    for card_data in seed_cards:
        card = HomeFeaturedServiceCard(
            section=section,
            title=card_data["title"],
            subtitle=card_data["subtitle"],
            image_alt=card_data["title"],
            cta_url=card_data["cta_url"],
            order=card_data["order"],
        )
        image_path = static_dir / card_data["filename"]
        if image_path.exists():
            card.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        card.save()
        cards.append(card)

    return cards


def _seed_awards_content():
    awards = list(Award.objects.order_by("order", "id"))
    if awards:
        return [award for award in awards if award.is_active]

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "year": "2024",
            "title": "Best CA Advisor of the Year",
            "source": "ICAI National Conference",
            "filename": "award_ceremony.png",
            "image_alt": "Best CA Advisor of the Year award",
            "featured": True,
            "order": 1,
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "National Business Council",
            "filename": "cert_gst_advisor.png",
            "image_alt": "Excellence in GST Advisory award",
            "featured": False,
            "order": 2,
        },
    ]

    created = []
    for card_data in seed_cards:
        award = Award(
            year=card_data["year"],
            title=card_data["title"],
            source=card_data["source"],
            image_alt=card_data["image_alt"],
            featured=card_data["featured"],
            order=card_data["order"],
        )
        image_path = static_dir / card_data["filename"]
        if image_path.exists():
            award.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        award.save()
        created.append(award)
    return created


def _seed_moments_milestones():
    items = list(MomentMilestone.objects.order_by("order", "id"))
    if items:
        return [item for item in items if item.is_active]

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_items = [
        {"title": "Workshop — Mumbai 2024", "filename": "workshop_mumbai.png", "is_tall": True, "order": 1},
        {"title": "Keynote Address", "filename": "keynote.png", "is_tall": False, "order": 2},
        {"title": "Client Advisory Session", "filename": "advisory.png", "is_tall": False, "order": 3},
        {"title": "Award Ceremony 2024", "filename": "award_ceremony.png", "is_tall": True, "order": 4},
        {"title": "Team Meeting", "filename": "team_meeting.png", "is_tall": False, "order": 5},
        {"title": "Professional Portrait", "filename": "portrait.png", "is_tall": True, "order": 6},
    ]

    created = []
    for item_data in seed_items:
        item = MomentMilestone(
            title=item_data["title"],
            image_alt=item_data["title"],
            is_tall=item_data["is_tall"],
            order=item_data["order"],
        )
        image_path = static_dir / item_data["filename"]
        if image_path.exists():
            item.image.save(
                item_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        item.save()
        created.append(item)
    return created


def _seed_faqs():
    faqs = list(FAQ.objects.filter(page="CCTS", is_active=True).order_by("order", "id"))
    if faqs:
        return faqs

    seed_faqs = [
        {
            "page": "CCTS",
            "question": "What is CCTS and why does it matter?",
            "answer": "CCTS converts carbon reduction into a regulated financial and compliance matter for Indian businesses.",
            "order": 1,
        },
        {
            "page": "CCTS",
            "question": "How does it affect accounting and taxation?",
            "answer": "Credits, obligations, timing, valuation, and disclosures can all affect books and tax positions.",
            "order": 2,
        },
        {
            "page": "CCTS",
            "question": "Who should read this guide?",
            "answer": "Business owners, CFOs, finance teams, tax professionals, and policy stakeholders.",
            "order": 3,
        },
        {
            "page": "CCTS",
            "question": "Is it relevant for SMEs?",
            "answer": "Yes, direct and supply-chain obligations can affect contracts, reporting, and valuation.",
            "order": 4,
        },
    ]
    for row in seed_faqs:
        FAQ.objects.create(**row)
    return list(FAQ.objects.filter(page="CCTS", is_active=True).order_by("order", "id"))


def _seed_ccts_services_content():
    section = CCTSServiceSection.objects.order_by("id").first()
    if section is None:
        section = CCTSServiceSection.objects.create(
            label="CCTS Specialization",
            title="Explore CCTS From Every Angle",
            description="Curated insights and practical frameworks for every stakeholder in India's Carbon Market.",
        )

    cards = list(section.cards.order_by("order", "id"))
    if cards:
        return section, [card for card in cards if card.is_active]

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "number": "01",
            "audience": "Chairman • MD • CEO • CFO",
            "title": "Could Your Company Face CCTS Penalties?",
            "summary": "Understand your obligations, reporting requirements, and potential liabilities under India's Carbon Credit Trading Scheme.",
            "filename": "ccts_story.png",
            "cta_text": "Explore the Legal Framework",
            "order": 1,
        },
        {
            "number": "02",
            "audience": "CA • CS • CMA • CFO",
            "title": "How Should Carbon Credits Be Accounted For?",
            "summary": "Navigate accounting, taxation, valuation, and disclosure requirements for Carbon Credit Certificates.",
            "filename": "ccts_story.png",
            "cta_text": "Explore the Financial Framework",
            "order": 2,
        },
        {
            "number": "03",
            "audience": "Student • Researcher • Journalist",
            "title": "How Does India's Carbon Market Work?",
            "summary": "Learn the fundamentals of carbon markets, compliance mechanisms, and India's net-zero journey.",
            "filename": "ccts_story.png",
            "cta_text": "Start Learning",
            "order": 3,
        },
    ]
    for card_data in seed_cards:
        card = CCTSServiceCard(
            section=section,
            number=card_data["number"],
            audience=card_data["audience"],
            title=card_data["title"],
            summary=card_data["summary"],
            image_alt=card_data["title"],
            cta_text=card_data["cta_text"],
            order=card_data["order"],
        )
        image_path = static_dir / card_data["filename"]
        if image_path.exists():
            card.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        card.save()
    return section, list(section.cards.filter(is_active=True).order_by("order", "id"))


def _seed_service_detail_hero_slides(service):
    slides = list(service.hero_slides.filter(is_active=True).order_by("order", "id"))
    if slides:
        return slides

    if not service.image:
        return []

    slide = ServiceDetailHeroSlide.objects.create(
        service=service,
        title=service.detail_heading or service.title,
        subtitle=service.detail_kicker,
        image=service.image,
        image_alt=service.image_alt or service.title,
        order=1,
        is_active=True,
    )
    return [slide]


def _seed_about_certifications_content():
    existing_certifications = list(AboutCertification.objects.order_by("order", "id"))
    if existing_certifications:
        return [certification for certification in existing_certifications if certification.is_active]

    certifications = []
    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_cards = [
        {
            "year": "2024",
            "title": "Best CA Advisor of the Year",
            "source": "ICAI National Conference",
            "filename": "cert_ca_advisor.png",
            "image_alt": "Certificate for Best CA Advisor of the Year",
            "order": 1,
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "Federation of Indian Chambers",
            "filename": "cert_gst_advisor.png",
            "image_alt": "Certificate for Excellence in GST Advisory",
            "order": 2,
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "filename": "cert_corp_recog_1.png",
            "image_alt": "Corporate Recognition Award certificate",
            "order": 3,
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "filename": "cert_corp_recog_2.png",
            "image_alt": "Corporate Recognition Award certificate",
            "order": 4,
        },
        {
            "year": "2022",
            "title": "Excellence in GST Advisory",
            "source": "Federation of Indian Chambers",
            "filename": "cert_corp_recog_3.png",
            "image_alt": "Certificate for Excellence in GST Advisory",
            "order": 5,
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "filename": "cert_membership.png",
            "image_alt": "Corporate Recognition Award certificate",
            "order": 6,
        },
        {
            "year": "2021",
            "title": "Corporate Recognition Award",
            "source": "ASSOCHAM India",
            "filename": "cert_diploma_trade.png",
            "image_alt": "Corporate Recognition Award certificate",
            "order": 7,
        },
    ]

    for card_data in seed_cards:
        certification = AboutCertification(
            year=card_data["year"],
            title=card_data["title"],
            source=card_data["source"],
            image_alt=card_data["image_alt"],
            order=card_data["order"],
        )
        image_path = static_dir / card_data["filename"]
        if image_path.exists():
            certification.image.save(
                card_data["filename"],
                ContentFile(image_path.read_bytes()),
                save=False,
            )
        certification.save()
        certifications.append(certification)

    return certifications


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


def _seed_testimonial_videos():
    existing_videos = list(TestimonialVideo.objects.order_by("order", "id"))
    if existing_videos:
        return [video for video in existing_videos if video.is_active]

    static_dir = Path(settings.BASE_DIR) / "website" / "static" / "images"
    seed_videos = [
        {
            "title": "Client Testimonial 01",
            "filename": "testimonial_video_1.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "order": 1,
        },
        {
            "title": "Client Testimonial 02",
            "filename": "testimonial_video_2.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "",
            "order": 2,
        },
        {
            "title": "Client Testimonial 03",
            "filename": "testimonial_video_3.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "",
            "order": 3,
        },
        {
            "title": "Client Testimonial 04",
            "filename": "testimonial_video_1.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "",
            "order": 4,
        },
        {
            "title": "Client Testimonial 05",
            "filename": "testimonial_video_2.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "",
            "order": 5,
        },
        {
            "title": "Client Testimonial 06",
            "filename": "testimonial_video_3.png",
            "thumbnail_alt": "Client testimonial video thumbnail",
            "youtube_url": "",
            "order": 6,
        },
    ]

    videos = []
    for video_data in seed_videos:
        video = TestimonialVideo(
            title=video_data["title"],
            thumbnail_alt=video_data["thumbnail_alt"],
            youtube_url=video_data["youtube_url"],
            order=video_data["order"],
        )
        thumbnail_path = static_dir / video_data["filename"]
        if thumbnail_path.exists():
            video.thumbnail.save(
                video_data["filename"],
                ContentFile(thumbnail_path.read_bytes()),
                save=False,
            )
        video.save()
        videos.append(video)

    return videos


def _seed_about_intro_content():
    section = AboutIntroSection.objects.order_by("id").first()
    if section is None:
        section = AboutIntroSection.objects.create(
            section_id="about",
            pretitle="Know Me Better",
            title="CA Ashwani Tayal",
            description=(
                "A seasoned Chartered Accountant with over 25 years of experience, CA Ashwani Tayal has been "
                "the trusted financial backbone for hundreds of businesses across India. Known for his practical "
                "approach, depth of knowledge, and commitment to client success, he brings clarity to complexity."
            ),
            poster_filename="figma_ashwani_video_poster.png",
            poster_alt="CA Ashwani Tayal video introduction",
            cta_url="#appointments",
        )

    if section.features.exists():
        return section

    features = [
        {"title": "Chartered Accountant", "icon_name": "user-check", "order": 1},
        {"title": "25+ Years Experience", "icon_name": "clock", "order": 2},
        {"title": "Mentor & Speaker", "icon_name": "video", "order": 3},
        {"title": "Trusted Business Advisor", "icon_name": "building-2", "order": 4},
    ]

    for feature in features:
        AboutIntroFeature.objects.create(section=section, **feature)

    return section


def home(request):
    """
    Renders the homepage with insights and consultation forms.
    """
    insights = _ensure_default_insights()

    form = ConsultationForm()
    home_service_section = _seed_home_services_content()
    home_service_cards = list(home_service_section.cards.all().order_by("order", "id"))
    featured_service_cards = _seed_home_featured_services()
    testimonial_videos = _seed_testimonial_videos()
    award_cards = _seed_awards_content()
    moments_milestones = _seed_moments_milestones()

    return render(
        request,
        "website/home.html",
        {
            "insights": insights,
            "form": form,
            "home_service_section": home_service_section,
            "home_service_cards": home_service_cards,
            "featured_service_cards": featured_service_cards,
            "testimonial_videos": testimonial_videos,
            "award_cards": award_cards,
            "moments_milestones": moments_milestones,
        },
    )


def services(request):
    """
    Renders the main services listing page with all service cards.
    """
    home_service_section = _seed_home_services_content()
    home_service_cards = list(home_service_section.cards.all().order_by("order", "id"))
    form = ConsultationForm()
    return render(
        request,
        "website/services.html",
        {
            "form": form,
            "home_service_section": home_service_section,
            "home_service_cards": home_service_cards,
        },
    )


def ccts(request):
    """
    Renders the Carbon Credit Trading Scheme (CCTS) page.
    """
    _ensure_default_insights()
    insights = list(Insight.objects.filter(category="CCTS").order_by("-published_date")[:3])
    form = ConsultationForm()
    ccts_service_section, ccts_service_cards = _seed_ccts_services_content()
    ccts_faqs = _seed_faqs()
    return render(
        request,
        "website/ccts.html",
        {
            "insights": insights,
            "form": form,
            "ccts_service_section": ccts_service_section,
            "ccts_service_cards": ccts_service_cards,
            "ccts_faqs": ccts_faqs,
            "blogs_url": reverse("website:blogs"),
        },
    )


def service_detail(request, slug):
    """
    Renders the reusable internal page for each dynamic service card.
    """
    home_service_section = _seed_home_services_content()
    service = get_object_or_404(HomeServiceCard, slug=slug)
    other_services = list(
        home_service_section.cards.exclude(pk=service.pk).order_by("order", "id")[:4]
    )
    hero_slides = _seed_service_detail_hero_slides(service)
    form = ConsultationForm()
    return render(
        request,
        "website/service_detail.html",
        {
            "form": form,
            "service": service,
            "other_services": other_services,
            "hero_slides": hero_slides,
        },
    )


def about(request):
    """
    Renders the detailed CA Ashwani Tayal biography, certifications, & values page.
    """
    form = ConsultationForm()
    about_hero_section = _seed_about_hero_content()
    about_hero_panels = list(about_hero_section.panels.all().order_by("order", "id"))
    about_intro_section = _seed_about_intro_content()
    about_intro_features = list(about_intro_section.features.all().order_by("order", "id"))
    about_certifications = _seed_about_certifications_content()
    return render(
        request,
        "website/about.html",
        {
            "form": form,
            "about_certifications": about_certifications,
            "about_hero_section": about_hero_section,
            "about_hero_panels": about_hero_panels,
            "about_intro_section": about_intro_section,
            "about_intro_features": about_intro_features,
        },
    )


def blogs(request):
    """
    Renders the comprehensive blogs & insights page.
    """
    insights = _ensure_default_insights()

    form = ConsultationForm()
    return render(request, "website/blogs.html", {"insights": insights, "form": form})


def contact(request):
    """
    Renders the contact page with the consultation form.
    """
    form = ConsultationForm()
    return render(request, "website/contact.html", {"form": form})


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
