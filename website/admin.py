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
    fields = ("title", "summary", "image", "image_alt", "badge_one", "badge_two", "link_url", "order")
    ordering = ("order", "id")


@admin.register(HomeServiceSection)
class HomeServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "label", "cta_text", "cta_url")
    search_fields = ("title", "label", "description")
    inlines = [HomeServiceCardInline]


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
