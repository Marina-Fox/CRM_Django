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
class ContractsList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка контрактов.
    """
    permission_required = ["contracts.view_contracts"]
    login_url = "/admin/login/"
    queryset = Contracts.objects.all()
    template_name = "contracts/contracts_list.html"
    context_object_name = "contracts"
