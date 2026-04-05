from django.urls import include, path

from .views import ServicesList, ServicesCreate, ServicesDetail

urlpatterns = [
    path("", ServicesList.as_view(), name="services_list"),
    path("new/", ServicesCreate.as_view(), name="services_create"),
    path("<int:pk>/", ServicesDetail.as_view(), name="services_detail"),
]
