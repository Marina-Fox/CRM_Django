from dataclasses import field

from django import forms

from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["first_name", "last_name", "patronymic", "phone", "email", "advertisement"]
