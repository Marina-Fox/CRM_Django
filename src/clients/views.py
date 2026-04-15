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
# Create your views here.
class LeadList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка потенуиальных клиентов.
    """
    permission_required = ["clients.view_lead"]
    login_url = "/admin/login/"
    queryset = Lead.objects.all()
    template_name = "clients/leads_list.html"
    context_object_name = "leads"
