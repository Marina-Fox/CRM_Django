from django.shortcuts import render
from django.views.generic import ListView

from .models import Services

# Create your views here.
class ServicesList(ListView):
    """
    Отображение списка услуг
    """
    model = Services
    paginate_by = 10
