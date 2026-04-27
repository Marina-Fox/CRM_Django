from django.urls import path

from .views import (
    CustomersList,
    # ContractsDetail,
    # ContractsCreate,
    # ContractsUptade,
    # ContractsDelete,
)

app_name = "customers"

urlpatterns = [
    path("", CustomersList.as_view(), name="customers_list"),
    # path("new/", ContractsCreate.as_view(), name="contracts_create"),
    # path("<int:pk>/", ContractsDetail.as_view(), name="contracts_detail"),
    # path("<int:pk>/edit/", ContractsUptade.as_view(), name="contracts_update"),
    # path("<int:pk>/delete/", ContractsDelete.as_view(), name="contracts_delete"),
]
