from django.contrib import admin
from .models import (
    ConsultationRequest,
    Insight,
    AALabelCard,
    HomeServiceCard,
    HomeServiceSection,
    AboutHeroSection,
    AboutHeroPanel,
    AboutIntroSection,
    AboutIntroFeature,
    AboutCertification,
    TestimonialVideo,
    HomeFeaturedServiceSection,
    HomeFeaturedServiceCard,
    Award,
    MomentMilestone,
    FAQ,
    CCTSServiceSection,
    CCTSServiceCard,
    ServiceDetailHeroSlide,
    SocialLink,
)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "service", "company", "created_at")
    list_filter = ("service", "created_at")
    search_fields = ("full_name", "email", "phone", "company", "message")
    ordering = ("-created_at",)


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date", "image_filename")
    list_filter = ("category", "published_date")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AALabelCard)
class AALabelCardAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "redirect_url")
    list_editable = ("order",)
    search_fields = ("title",)


class HomeServiceCardInline(admin.StackedInline):
    model = HomeServiceCard
    extra = 0
    fields = (
        "title",
        "slug",
        "summary",
        "image",
        "image_alt",
        "badge_one",
        "badge_two",
        "link_url",
        "detail_kicker",
        "detail_heading",
        "detail_intro",
        "detail_body",
        "detail_points",
        "order",
    )
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "id")


class ServiceDetailHeroSlideInline(admin.TabularInline):
    model = ServiceDetailHeroSlide
    extra = 0
    fields = ("title", "subtitle", "image", "image_alt", "order", "is_active")
    ordering = ("order", "id")


@admin.register(HomeServiceSection)
class HomeServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "label", "cta_text", "cta_url")
    search_fields = ("title", "label", "description")
    inlines = [HomeServiceCardInline]


@admin.register(HomeServiceCard)
class HomeServiceCardAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "link_url")
    list_filter = ("section",)
    search_fields = ("title", "summary", "badge_one", "badge_two")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceDetailHeroSlideInline]
    ordering = ("section", "order", "id")


class AboutHeroPanelInline(admin.TabularInline):
    model = AboutHeroPanel
    extra = 0
    fields = ("number", "title", "subtitle", "icon_name", "tone", "order")
    ordering = ("order", "id")


@admin.register(AboutHeroSection)
class AboutHeroSectionAdmin(admin.ModelAdmin):
    list_display = ("pretitle", "title_line_one", "title_line_two", "title_highlight")
    search_fields = ("pretitle", "title_line_one", "title_line_two", "title_highlight", "description")
    inlines = [AboutHeroPanelInline]


class AboutIntroFeatureInline(admin.TabularInline):
    model = AboutIntroFeature
    extra = 0
    fields = ("title", "icon_name", "order")
    ordering = ("order", "id")


@admin.register(AboutIntroSection)
class AboutIntroSectionAdmin(admin.ModelAdmin):
    list_display = ("pretitle", "title", "section_id", "cta_url")
    search_fields = ("pretitle", "title", "description", "section_id")
    inlines = [AboutIntroFeatureInline]


@admin.register(AboutCertification)
class AboutCertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "source", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "year")
    search_fields = ("title", "source", "image_alt")
    ordering = ("order", "id")


@admin.register(TestimonialVideo)
class TestimonialVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "youtube_url", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "thumbnail_alt", "youtube_url")
    ordering = ("order", "id")


class HomeFeaturedServiceCardInline(admin.TabularInline):
    model = HomeFeaturedServiceCard
    extra = 0
    fields = ("title", "subtitle", "image", "image_alt", "cta_url", "order", "is_active")
    ordering = ("order", "id")


@admin.register(HomeFeaturedServiceSection)
class HomeFeaturedServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [HomeFeaturedServiceCardInline]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "source", "order", "is_active", "featured")
    list_editable = ("order", "is_active", "featured")
    list_filter = ("is_active", "year", "featured")
    search_fields = ("title", "source", "image_alt")
    ordering = ("order", "id")


@admin.register(MomentMilestone)
class MomentMilestoneAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_tall", "is_active")
    list_editable = ("order", "is_tall", "is_active")
    list_filter = ("is_tall", "is_active")
    search_fields = ("title", "image_alt")
    ordering = ("order", "id")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "page", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("page", "is_active")
    search_fields = ("question", "answer")
    ordering = ("page", "order", "id")


class CCTSServiceCardInline(admin.TabularInline):
    model = CCTSServiceCard
    extra = 0
    fields = (
        "number",
        "audience",
        "title",
        "summary",
        "image",
        "image_alt",
        "cta_text",
        "cta_url",
        "order",
        "is_active",
    )
    ordering = ("order", "id")


@admin.register(CCTSServiceSection)
class CCTSServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "label")
    search_fields = ("title", "label", "description")
    inlines = [CCTSServiceCardInline]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("label", "url", "icon_name")
    ordering = ("order", "id")
