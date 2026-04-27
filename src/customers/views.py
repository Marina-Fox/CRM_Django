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


# Create your views here.
class CustomersList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    """
    Отображение списка активных клиентов.
    """
    permission_required = ["customers.view_customers"]
    login_url = "/admin/login/"
    queryset = Customers.objects.all()
    template_name = "customers/customers_list.html"
    context_object_name = "customers"
