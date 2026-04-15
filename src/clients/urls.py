from django.urls import include, path

from .views import LeadList

app_name = "clients"

urlpatterns = [
    path("", LeadList.as_view(), name="clients_list"),
    # path("new/", AdvertisementCreate.as_view(), name="ad_create"),
    # path("<int:pk>/", AdvertisementDetail.as_view(), name="ad_detail"),
    # path("<int:pk>/edit/", AdvertisementUpdate.as_view(), name="ad_update"),
    # path("<int:pk>/delete/", AdvertisementDelete.as_view(), name="ad_delete"),
]
