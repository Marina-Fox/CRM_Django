from django.urls import include, path

from .views import LeadList, LeadDetail, LeadCreate, LeadUpdate, LeadDelete

app_name = "clients"

urlpatterns = [
    path("", LeadList.as_view(), name="clients_list"),
    path("new/", LeadCreate.as_view(), name="clients_create"),
    path("<int:pk>/", LeadDetail.as_view(), name="clients_detail"),
    path("<int:pk>/edit/", LeadUpdate.as_view(), name="clients_update"),
    path("<int:pk>/delete/", LeadDelete.as_view(), name="clients_delete"),
]
