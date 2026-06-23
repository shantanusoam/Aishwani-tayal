from django import forms
from .models import ConsultationRequest


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ["full_name", "email", "phone", "service", "company", "message"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300",
                    "placeholder": "Rajesh Mehta",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300",
                    "placeholder": "rajesh@company.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300",
                    "placeholder": "+91 98765 43210",
                }
            ),
            "service": forms.Select(
                attrs={
                    "class": "w-full px-3 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300",
                }
            ),
            "company": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300",
                    "placeholder": "Mehta Enterprises",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all duration-300 h-28 resize-none",
                    "placeholder": "Briefly describe your requirement...",
                }
            ),
        }
