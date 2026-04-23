from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import Lead
from .form import LeadForm


# Create your views here.
class LeadList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка потенциальных клиентов.
    """

    permission_required = ["clients.view_lead"]
    login_url = "/admin/login/"
    queryset = Lead.objects.all()
    template_name = "clients/leads_list.html"
    context_object_name = "leads"


class LeadDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """
    Информация о потенциальном клиенте.
    """

    permission_required = ["clients.view_lead"]
    login_url = "/admin/login/"
    model = Lead
    template_name = "clients/leads_detail.html"


class LeadCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Создание нового потенциального клиента.
    """

    permission_required = ["clients.add_lead"]
    login_url = "/admin/login/"
    model = Lead
    form_class = LeadForm
    template_name = "clients/leads_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("clients:clients_create")
