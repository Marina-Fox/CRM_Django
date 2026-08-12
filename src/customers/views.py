from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Customers
from .form import CustomersForm


# Create your views here.
class CustomersList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Отображение списка активных клиентов.
    """

    permission_required = ["customers.view_customers"]
    login_url = "/users/login/"
    queryset = Customers.objects.all()
    template_name = "customers/customers_list.html"
    context_object_name = "customers"


class CustomersDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Информация о потенциальном клиенте.
    """

    permission_required = ["customers.view_customers"]
    login_url = "/users/login/"
    model = Customers
    template_name = "customers/customers_detail.html"


class CustomersCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Добавление нового активного клиента.
    """

    permission_required = ["customers.add_customers"]
    login_url = "/users/login/"
    model = Customers
    form_class = CustomersForm
    template_name = "customers/customers_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("customers:customers_detail", args=[self.object.pk])


class CustomersUptade(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Редактирование активного клиента.
    """

    permission_required = ["customers.change_customers"]
    login_url = "/users/login/"
    model = Customers
    form_class = CustomersForm
    template_name = "customers/customers_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("customers:customers_detail", args=[self.object.pk])


class CustomersDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Удаление активного клиента.
    """

    permission_required = ["customers.delete_customers"]
    login_url = "/users/login/"
    model = Customers
    template_name = "customers/customers_delete.html"
    success_url = reverse_lazy("customers:customers_list")
