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
from .form import AdvertisementForm


# Create your views here.
class AdvertisementList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка рекламных кампаний.
    """

    permission_required = ["ad_campaign.view_advertisement"]
    login_url = "/admin/login/"
    queryset = Advertisement.objects.all()
    context_object_name = "ads"
    template_name = "ad_campaign/ads_list.html"


class AdvertisementCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Создание новой рекламной кампании.
    """

    permission_required = ["ad_campaign.add_advertisement"]
    login_url = "/admin/login/"
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ad_campaign/ads_create.html"

    def get_success_url(self):
        return reverse_lazy("ad_campaign:ad_detail", args=[self.object.pk])


class AdvertisementDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Информация о рекламной кампании.
    """
    permission_required = ["ad_campaign.view_advertisement"]
    login_url = "/admin/login/"
    model = Advertisement
    template_name = "ad_campaign/ads_detail.html"


class AdvertisementUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование рекламной кампании.
    """
    permission_required = ["change_advertisement"]
    login_url = "/admin/login/"
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ad_campaign/ads_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("ad_campaign:ad_detail", args=[self.object.pk])
