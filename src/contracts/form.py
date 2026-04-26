from django import forms

from .models import Contracts


class ContractsForm(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = ["title", "service", "file_doc", "end_date", "cost"]
