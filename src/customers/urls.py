from django.urls import path

from .views import (
    CustomersList,
    CustomersCreate,
    CustomersDetail,
    CustomersUptade,
    CustomersDelete,
)

app_name = "customers"

urlpatterns = [
    path("", CustomersList.as_view(), name="customers_list"),
    path("new/", CustomersCreate.as_view(), name="customers_create"),
    path("<int:pk>/", CustomersDetail.as_view(), name="customers_detail"),
    path("<int:pk>/edit/", CustomersUptade.as_view(), name="customers_update"),
    path("<int:pk>/delete/", CustomersDelete.as_view(), name="customers_delete"),
]
