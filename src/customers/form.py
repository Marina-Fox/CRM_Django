from django import forms

from .models import Customers


class CustomersForm(forms.ModelForm):
    class Mete:
        model = Customers
        fields = ["lead", "contract"]
