from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Advertisement
from ...services.models import Services


# Create your tests here.
class TestAdvertisementListView(TestCase):
    """
    Тесты для представленния AdvertisementList.
    """

    def setUp(self) -> None:
        self.service_1 = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.service_2 = Services.objects.create(
            title="Title 2",
            description="descrip 2",
            cost=Decimal("1500.00"),
        )
        self.ad_campaign_1 = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service_1,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.ad_campaign_2 = Advertisement.objects.create(
            title="Test 2",
            service=self.service_2,
            promotion_channel="Test 2 ad camp",
            budget=Decimal("5000.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Advertisement)
        self.permis = Permission.objects.get(
            codename="view_advertisement",
            content_type=con_type,
        )
        self.url = reverse("ad_campaign:ad_list")

    def test_get_advertisement_list(self):
        "Проверка получения списка рекламных кампаний."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertQuerySetEqual(
            respons.context["ads"],
            [self.ad_campaign_1, self.ad_campaign_2],
            ordered=False,
        )

    def test_get_advertisement_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_list_permis(self):
        "Проверка, что пользователь без разрешения view_advertisement не может просмотреть список рекламных кампаний."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestAdvertisementCreate(TestCase):
    """
    Тесты для представленния AdvertisementCreate.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Advertisement)
        self.permis_add = Permission.objects.get(
            codename="add_advertisement",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_advertisement",
            content_type=con_type,
        )
        self.url = reverse("ad_campaign:ad_create")

    def test_get_advertisement_create(self):
        "Проверка получения формы для создания рекламной кампании."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "ad_campaign/ads_create.html")

    def test_post_advertisement_create(self):
        "Проверка создания новой рекламной кампании."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test ad camp",
            "service": self.service.pk,
            "promotion_channel": "Test 1",
            "budget": Decimal("500.00"),
        }
        respons = self.client.post(self.url, data=data, format="json")

        self.assertEqual(respons.status_code, 302)

        advertisement = Advertisement.objects.first()
        self.assertRedirects(
            respons, reverse("ad_campaign:ad_detail", args=[advertisement.pk])
        )

    def test_get_advertisement_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_create_permis(self):
        "Проверка, что пользователь без разрешения add_advertisement не может создать новую рекламную кампанию."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestAdvertisementDetail(TestCase):
    """
    Тесты для представленния AdvertisementDetail.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Advertisement)
        self.permis = Permission.objects.get(
            codename="view_advertisement",
            content_type=con_type,
        )
        self.url = reverse("ad_campaign:ad_detail", args=[self.ad_campaign.pk])

    def test_get_advertisement_detail(self):
        "Проверка получения страницы деталей рекламной кампании."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "ad_campaign/ads_detail.html")
        self.assertEqual(respons.context["object"], self.ad_campaign)

    def test_get_advertisement_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_detail_permis(self):
        "Проверка, что пользователь без разрешения view_advertisement не может просмотреть детальную страницу рекламной кампании."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestAdvertisementUpdate(TestCase):
    """
    Тесты для представленния AdvertisementUpdate.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Advertisement)
        self.permis_update = Permission.objects.get(
            codename="change_advertisement",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_advertisement",
            content_type=con_type,
        )
        self.url = reverse("ad_campaign:ad_update", args=[self.ad_campaign.pk])

    def test_get_advertisement_update(self):
        "Проверка получения формы для обновления рекламной кампании."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "ad_campaign/ads_edit.html")

    def test_post_advertisement_update(self):
        "Проверка внесения изменений в рекламную кампанию."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test amp",
            "service": self.service.pk,
            "promotion_channel": "Test 1",
            "budget": Decimal("500.00"),
        }
        respons = self.client.post(self.url, data=data, format="json")

        self.assertEqual(respons.status_code, 302)

        advertisement = Advertisement.objects.first()
        self.assertRedirects(
            respons, reverse("ad_campaign:ad_detail", args=[advertisement.pk])
        )

    def test_get_advertisement_update_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_update_permis(self):
        "Проверка, что пользователь без разрешения change_advertisement не может изменить рекламную кампанию."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestAdvertisementDelete(TestCase):
    """
    Тесты для представленния AdvertisementDelete.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=self.service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Advertisement)
        self.permis_del = Permission.objects.get(
            codename="delete_advertisement",
            content_type=con_type,
        )
        self.permis_view = Permission.objects.get(
            codename="view_advertisement",
            content_type=con_type,
        )
        self.url = reverse("ad_campaign:ad_delete", args=[self.ad_campaign.pk])

    def test_get_advertisement_delete(self):
        "Проверка получения формы для удаления рекламной кампании."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "ad_campaign/ads_delete.html")

    def test_delete_advertisement(self):
        "Проверка удаления рекламной кампании."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("ad_campaign:ad_list"))

    def test_get_advertisement_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_services не может удалить рекламную кампанию."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)
