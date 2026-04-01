from django.urls import include, path

from .views import ServicesList

urlpatterns = [
    path("", ServicesList.as_view(), name="services_list")
]
