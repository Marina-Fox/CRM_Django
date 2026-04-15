from django.urls import path
from .views import AdvertisementList, AdvertisementCreate, AdvertisementDetail, AdvertisementUpdate

app_name = "ad_campaign"

urlpatterns = [
    path("", AdvertisementList.as_view(), name="ad_list"),
    path("new/", AdvertisementCreate.as_view(), name="ad_create"),
    path("<int:pk>/", AdvertisementDetail.as_view(), name="ad_detail"),
    path("<int:pk>/edit/", AdvertisementUpdate.as_view(), name="ad_update"),
    # path("<int:pk>/delete/", ServicesDelete.as_view(), name="ad_delete"),
]
