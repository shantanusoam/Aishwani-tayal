from django.db import models
from django.utils.text import slugify


class ConsultationRequest(models.Model):
    SERVICE_CHOICES = [
        ("X-RAY", "X-RAY Framework - Investigation & Diagnosis"),
        ("CCTS", "CCTS - Measure & Monetize"),
        ("TAX", "Tax Planning & Audit"),
        ("GST", "GST Advisory & ITC"),
        ("BUSINESS", "Business Advisory & Growth"),
        ("OTHER", "Other Financial Services"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default="X-RAY")
    company = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service} ({self.created_at.strftime('%Y-%m-%d')})"


class Insight(models.Model):
    CATEGORY_CHOICES = [
        ("TAX", "Tax Planning"),
        ("GST", "GST"),
        ("BIZ", "Business Advisory"),
        ("LAW", "Compliance"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="TAX")
    published_date = models.DateField()
    summary = models.TextField()
    read_more_link = models.CharField(max_length=250, default="#")
    image_filename = models.CharField(max_length=100)  # e.g., blog_tax.png

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

