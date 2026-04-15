from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Services
from .form import ServicesForm


# Create your views here.
class ServicesList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка услуг.
    """

    permission_required = ["services.view_services"]
    login_url = "/admin/login/"
    queryset = Services.objects.all()
    context_object_name = "services"
    # paginate_by = 10
    # ordering = ["created_at"]


class ServicesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Создание новой услуги.
    """

    permission_required = ["services.add_services"]
    login_url = "/admin/login/"
    model = Services
    form_class = ServicesForm
    template_name = "services/services_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("services:services_detail", args=[self.object.pk])


class ServicesDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Информация о выбранной услуге.
    """

    permission_required = ["services.view_services"]
    login_url = "/admin/login/"
    model = Services
    template_name = "services/services_detail.html"


class ServicesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирование услуги.
    """

    permission_required = ["services.change_services"]
    login_url = "/admin/login/"
    model = Services
    form_class = ServicesForm
    template_name = "services/services_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("services:services_detail", args=[self.object.pk])


class ServicesDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """
    Удаление услуги
    """

    permission_required = ["services.delete_services"]
    login_url = "/admin/login/"
    model = Services
    template_name = "services/services_delete.html"
    success_url = reverse_lazy("services:services_list")
