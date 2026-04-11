from django.urls import include, path

from .views import ServicesList, ServicesCreate, ServicesDetail, ServicesUpdate, ServicesDelete

app_name = "services"

urlpatterns = [
    path("", ServicesList.as_view(), name="services_list"),
    path("new/", ServicesCreate.as_view(), name="services_create"),
    path("<int:pk>/", ServicesDetail.as_view(), name="services_detail"),
    path("<int:pk>/edit/", ServicesUpdate.as_view(), name="services_update"),
    path("<int:pk>/delete/", ServicesDelete.as_view(), name="services_delete"),
]
