from django.urls import path

from .views import ContractsList, ContractsDetail

app_name = "contracts"

urlpatterns = [
    path("", ContractsList.as_view(), name="contracts_list"),
    # path("new/", LeadCreate.as_view(), name="contracts_create"),
    path("<int:pk>/", ContractsDetail.as_view(), name="contracts_detail"),
    # path("<int:pk>/edit/", LeadUpdate.as_view(), name="clients_update"),
    # path("<int:pk>/delete/", LeadDelete.as_view(), name="clients_delete"),
]
