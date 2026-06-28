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
        ("CCTS", "CCTS"),
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
    slug = models.SlugField(max_length=170, unique=True, null=True, blank=True)
    summary = models.TextField()
    image = models.ImageField(upload_to="home_services/")
    image_alt = models.CharField(max_length=180, blank=True)
    badge_one = models.CharField(max_length=80)
    badge_two = models.CharField(max_length=80)
    link_url = models.CharField(max_length=250, default="/services/")
    detail_kicker = models.CharField(max_length=120, default="Strategic Advisory")
    detail_heading = models.CharField(max_length=180, blank=True)
    detail_intro = models.TextField(blank=True)
    detail_body = models.TextField(blank=True)
    detail_points = models.TextField(
        blank=True,
        help_text="One service-detail bullet per line.",
    )
    order = models.PositiveIntegerField(default=0, help_text="Order in which cards are displayed.")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Home Service Card"
        verbose_name_plural = "Home Service Cards"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "service"
            candidate = base_slug
            suffix = 2
            while HomeServiceCard.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate

        if not self.detail_heading:
            self.detail_heading = self.title

        super().save(*args, **kwargs)

    @property
    def detail_points_list(self):
        return [point.strip() for point in self.detail_points.splitlines() if point.strip()]


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


class AboutIntroSection(models.Model):
    section_id = models.CharField(max_length=50, default="about")
    pretitle = models.CharField(max_length=120, default="Know Me Better")
    title = models.CharField(max_length=120, default="CA Ashwani Tayal")
    description = models.TextField(
        default=(
            "A seasoned Chartered Accountant with over 25 years of experience, CA Ashwani Tayal has been "
            "the trusted financial backbone for hundreds of businesses across India. Known for his practical "
            "approach, depth of knowledge, and commitment to client success, he brings clarity to complexity."
        )
    )
    poster_filename = models.CharField(max_length=120, default="figma_ashwani_video_poster.png")
    poster_alt = models.CharField(max_length=180, default="CA Ashwani Tayal video introduction")
    cta_url = models.CharField(max_length=250, default="#appointments")

    class Meta:
        verbose_name = "About Intro Section"
        verbose_name_plural = "About Intro Sections"

    def __str__(self):
        return self.title


class AboutIntroFeature(models.Model):
    section = models.ForeignKey(
        AboutIntroSection,
        on_delete=models.CASCADE,
        related_name="features",
    )
    title = models.CharField(max_length=120)
    icon_name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "About Intro Feature"
        verbose_name_plural = "About Intro Features"

    def __str__(self):
        return self.title


class AboutCertification(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    source = models.CharField(max_length=180)
    image = models.ImageField(upload_to="about_certifications/")
    image_alt = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "About Certification"
        verbose_name_plural = "About Certifications"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return self.image.url if self.image else ""


class TestimonialVideo(models.Model):
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to="testimonial_videos/")
    thumbnail_alt = models.CharField(max_length=180, blank=True)
    youtube_url = models.URLField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Testimonial Video"
        verbose_name_plural = "Testimonial Videos"

    def __str__(self):
        return self.title


class HomeFeaturedServiceSection(models.Model):
    title = models.CharField(max_length=150, default="Home Featured Services")

    class Meta:
        verbose_name = "Home Featured Service Section"
        verbose_name_plural = "Home Featured Service Sections"

    def __str__(self):
        return self.title


class HomeFeaturedServiceCard(models.Model):
    section = models.ForeignKey(
        HomeFeaturedServiceSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="home_featured_services/")
    image_alt = models.CharField(max_length=180, blank=True)
    cta_url = models.CharField(max_length=250, default="/services/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Home Featured Service Card"
        verbose_name_plural = "Home Featured Service Cards"

    def __str__(self):
        return self.title


class Award(models.Model):
    year = models.CharField(max_length=10)
    title = models.CharField(max_length=150)
    source = models.CharField(max_length=180)
    image = models.ImageField(upload_to="awards/")
    image_alt = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Award"
        verbose_name_plural = "Awards"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return self.image.url if self.image else ""


class MomentMilestone(models.Model):
    title = models.CharField(max_length=180)
    image = models.ImageField(upload_to="moments_milestones/")
    image_alt = models.CharField(max_length=180, blank=True)
    is_tall = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Moment & Milestone"
        verbose_name_plural = "Moments & Milestones"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return self.image.url if self.image else ""


class FAQ(models.Model):
    PAGE_CHOICES = [
        ("HOME", "Home"),
        ("CCTS", "CCTS"),
        ("GENERAL", "General"),
    ]

    page = models.CharField(max_length=20, choices=PAGE_CHOICES, default="CCTS")
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class CCTSServiceSection(models.Model):
    label = models.CharField(max_length=120, default="CCTS Services")
    title = models.CharField(max_length=180, default="Explore CCTS From Every Angle")
    description = models.TextField(
        default="Curated insights and practical frameworks for every stakeholder in India's carbon market."
    )

    class Meta:
        verbose_name = "CCTS Service Section"
        verbose_name_plural = "CCTS Service Sections"

    def __str__(self):
        return self.title


class CCTSServiceCard(models.Model):
    section = models.ForeignKey(
        CCTSServiceSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    number = models.CharField(max_length=10, default="01")
    audience = models.CharField(max_length=180)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    image = models.ImageField(upload_to="ccts_services/", blank=True)
    image_alt = models.CharField(max_length=180, blank=True)
    cta_text = models.CharField(max_length=100, default="Learn More")
    cta_url = models.CharField(max_length=250, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "CCTS Service Card"
        verbose_name_plural = "CCTS Service Cards"

    def __str__(self):
        return self.title


class ServiceDetailHeroSlide(models.Model):
    service = models.ForeignKey(
        HomeServiceCard,
        on_delete=models.CASCADE,
        related_name="hero_slides",
    )
    title = models.CharField(max_length=160, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="service_hero_slides/")
    image_alt = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service Detail Hero Slide"
        verbose_name_plural = "Service Detail Hero Slides"

    def __str__(self):
        return self.title or self.service.title

    @property
    def image_url(self):
        return self.image.url if self.image else ""


class SocialLink(models.Model):
    label = models.CharField(max_length=80, default="Linktree")
    url = models.URLField(max_length=500, default="https://linktr.ee/ca_ashwanitayal")
    icon_name = models.CharField(max_length=50, default="link")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.label
