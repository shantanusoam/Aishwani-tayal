from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import datetime

from .models import Insight, ConsultationRequest
from .forms import ConsultationForm


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
    return render(request, "website/home.html", {"insights": insights, "form": form})


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

