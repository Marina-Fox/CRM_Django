from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Contracts
from .form import ContractsForm


# Create your views here.
class ContractsList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Отображение списка контрактов.
    """

    permission_required = ["contracts.view_contracts"]
    login_url = "/users/login/"
    queryset = Contracts.objects.all()
    template_name = "contracts/contracts_list.html"
    context_object_name = "contracts"


class ContractsDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Информация о контракте.
    """

    permission_required = ["contracts.view_contracts"]
    login_url = "/users/login/"
    model = Contracts
    template_name = "contracts/contracts_detail.html"


class ContractsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Добавление нового контракта.
    """

    permission_required = ["contracts.add_contracts"]
    login_url = "/users/login/"
    model = Contracts
    form_class = ContractsForm
    template_name = "contracts/contracts_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("contracts:contracts_detail", args=[self.object.pk])


class ContractsUptade(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Редактирование контракта.
    """

    permission_required = ["contracts.change_contracts"]
    login_url = "/users/login/"
    model = Contracts
    form_class = ContractsForm
    template_name = "contracts/contracts_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("contracts:contracts_detail", args=[self.object.pk])


class ContractsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Удаление контракта.
    """

    permission_required = ["contracts.delete_contracts"]
    login_url = "/users/login/"
    model = Contracts
    template_name = "contracts/contracts_delete.html"
    success_url = reverse_lazy("contracts:contracts_list")
