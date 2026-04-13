from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Advertisement

# Create your views here.
class AdvertisementList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    "Отображение списка рекламных кампаний."
    permission_required = ["ad_campaign.view_advertisement"]
    login_url = "/admin/login/"
    queryset = Advertisement.objects.all()
    context_object_name = "ad"
    template_name = "ad_campaign/ads_list.html"
