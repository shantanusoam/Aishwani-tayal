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


class AALabelCard(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="aa_labels/")
    redirect_url = models.CharField(max_length=250, default="#")
    order = models.PositiveIntegerField(default=0, help_text="Order in which cards are displayed.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "A&A Label Card"
        verbose_name_plural = "A&A Label Cards"

    def __str__(self):
        return self.title


class HomeServiceSection(models.Model):
    label = models.CharField(max_length=120, default="What We Offer")
    title = models.CharField(max_length=180, default="Expertise That Drives Real Results")
    description = models.TextField(
        default="Comprehensive financial solutions designed to support every stage of your business journey."
    )
    cta_text = models.CharField(max_length=80, default="View All Services")
    cta_url = models.CharField(max_length=250, default="/services/")

    class Meta:
        verbose_name = "Home Service Section"
        verbose_name_plural = "Home Service Sections"

    def __str__(self):
        return self.title


class HomeServiceCard(models.Model):
    section = models.ForeignKey(
        HomeServiceSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    title = models.CharField(max_length=150)
    summary = models.TextField()
    image = models.ImageField(upload_to="home_services/")
    image_alt = models.CharField(max_length=180, blank=True)
    badge_one = models.CharField(max_length=80)
    badge_two = models.CharField(max_length=80)
    link_url = models.CharField(max_length=250, default="/services/")
    order = models.PositiveIntegerField(default=0, help_text="Order in which cards are displayed.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Home Service Card"
        verbose_name_plural = "Home Service Cards"

    def __str__(self):
        return self.title


class AboutHeroSection(models.Model):
    pretitle = models.CharField(max_length=120, default="KNOW ME BETTER")
    title_line_one = models.CharField(max_length=120, default="Experience.")
    title_line_two = models.CharField(max_length=120, default="Expertise.")
    title_highlight = models.CharField(max_length=120, default="Impact.")
    description = models.TextField(
        default="A journey of trust, learning and leadership that has empowered businesses, inspired professionals and created lasting impact."
    )
    image_filename = models.CharField(max_length=120, default="about_hero_portrait.png")
    image_alt = models.CharField(max_length=180, default="CA Ashwani Tayal")

    class Meta:
        verbose_name = "About Hero Section"
        verbose_name_plural = "About Hero Section"

    def __str__(self):
        return self.pretitle


class AboutHeroPanel(models.Model):
    TONE_CHOICES = [
        ("navy", "Navy"),
        ("blue", "Blue"),
        ("midblue", "Mid Blue"),
        ("gold", "Gold"),
        ("lightgold", "Light Gold"),
    ]

    section = models.ForeignKey(
        AboutHeroSection,
        on_delete=models.CASCADE,
        related_name="panels",
    )
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=120, blank=True)
    icon_name = models.CharField(max_length=50)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default="navy")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "About Hero Panel"
        verbose_name_plural = "About Hero Panels"

    def __str__(self):
        return f"{self.number} - {self.title}"
