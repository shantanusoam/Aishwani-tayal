from django.contrib import admin
from .models import ConsultationRequest, Insight


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

