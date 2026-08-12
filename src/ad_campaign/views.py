from decimal import Decimal

from django.db.models import Count, DecimalField, Sum, F, ExpressionWrapper
from django.db.models.functions import Round
from django.db.models.query import QuerySet
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
class AdvertisementList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Отображение списка рекламных кампаний.
    """

    permission_required = ["ad_campaign.view_advertisement"]
    login_url = "/users/login/"
    queryset = Advertisement.objects.all()
    context_object_name = "ads"
    template_name = "ad_campaign/ads_list.html"


class AdvertisementCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Создание новой рекламной кампании.
    """

    permission_required = ["ad_campaign.add_advertisement"]
    login_url = "/users/login/"
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ad_campaign/ads_create.html"

    def get_success_url(self):
        return reverse_lazy("ad_campaign:ad_detail", args=[self.object.pk])


class AdvertisementDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Информация о рекламной кампании.
    """

    permission_required = ["ad_campaign.view_advertisement"]
    login_url = "/users/login/"
    model = Advertisement
    template_name = "ad_campaign/ads_detail.html"


class AdvertisementUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Редактирование рекламной кампании.
    """

    permission_required = ["ad_campaign.change_advertisement"]
    login_url = "/users/login/"
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "ad_campaign/ads_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("ad_campaign:ad_detail", args=[self.object.pk])


class AdvertisementDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Удаление рекламной кампании.
    """

    permission_required = ["ad_campaign.delete_advertisement"]
    login_url = "/users/login/"
    model = Advertisement
    template_name = "ad_campaign/ads_delete.html"
    success_url = reverse_lazy("ad_campaign:ad_list")


class Statistic(LoginRequiredMixin, ListView):
    """
    Просмотр статистики рекламных кампаний.
    """

    login_url = "/users/login/"
    context_object_name = "ads"
    template_name = "ad_campaign/ads_statistic.html"

    def get_queryset(self) -> QuerySet:
        money_field = DecimalField(
            max_digits=14,
            decimal_places=2,
        )

        return (Advertisement.objects
                .annotate(
                    leads_count=Count("leads", distinct=True),
                    customers_count=Count("leads__customers", distinct=True),
                    revenue=Sum(
                        "leads__customers__contract__cost",
                        default=Decimal("0.00"),
                        output_field=money_field,
                    )
                )
                .annotate(
                    profit=Round(
                        ExpressionWrapper(
                            (F("revenue") - F("budget")) / F("budget") * 100,
                            output_field=money_field,
                        )
                    )
                )
                .order_by("title")
            )
