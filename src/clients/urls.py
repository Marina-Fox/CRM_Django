from django.urls import include, path

from .views import LeadList, LeadDetail, LeadCreate

app_name = "clients"

urlpatterns = [
    path("", LeadList.as_view(), name="clients_list"),
    path("new/", LeadCreate.as_view(), name="clients_create"),
    path("<int:pk>/", LeadDetail.as_view(), name="clients_detail"),
    # path("<int:pk>/edit/", AdvertisementUpdate.as_view(), name="ad_update"),
    # path("<int:pk>/delete/", AdvertisementDelete.as_view(), name="ad_delete"),
]
