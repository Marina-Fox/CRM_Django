from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Services
from .form import ServicesForm

# Create your views here.
class ServicesList(PermissionRequiredMixin, ListView):
    """
    Отображение списка услуг
    """
    permission_required = ["services.view_services"]
    queryset = Services.objects.all()
    context_object_name = "services"
    # paginate_by = 10


class ServicesCreate(CreateView):
    """
    Создание новой услуги
    """
    model = Services
    form_class = ServicesForm
    template_name = "services/services_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("services_detail", kwargs={"pk": self.object.pk})


class ServicesDetail(DetailView):
    """
    Информация о выбранной услуге
    """
    model = Services
    template_name = "services/services_detail.html"


class ServicesUpdate(UpdateView):
    """
    Редактирование услуги
    """
    model = Services
    form_class = ServicesForm
    template_name = "services/services_edit.html"

    def get_success_url(self) -> str:
        return reverse_lazy("services_detail", kwargs={"pk": self.object.pk})


class ServicesDelete(DeleteView):
    """
    Удаление услуги
    """
    model = Services
    template_name = "services/services_delete.html"
    success_url = reverse_lazy("services_list")
