from django.urls import path

from .views import (
    AdvertisementList,
    AdvertisementCreate,
    AdvertisementDetail,
    AdvertisementUpdate,
    AdvertisementDelete,
    Statistic,
)

app_name = "ad_campaign"

urlpatterns = [
    path("", AdvertisementList.as_view(), name="ad_list"),
    path("new/", AdvertisementCreate.as_view(), name="ad_create"),
    path("<int:pk>/", AdvertisementDetail.as_view(), name="ad_detail"),
    path("<int:pk>/edit/", AdvertisementUpdate.as_view(), name="ad_update"),
    path("<int:pk>/delete/", AdvertisementDelete.as_view(), name="ad_delete"),
    path("statistic/", Statistic.as_view(), name="statistic"),
]
