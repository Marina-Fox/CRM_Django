from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Advertisement


class BaseAdvertisementTestCase(TestCase):
    """
    Базовый класс для тестов приложения ad_campaign.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="pass")
        content_type = ContentType.objects.get_for_model(Advertisement)
        cls.permis_view = Permission.objects.get(
            codename="view_advertisement",
            content_type=content_type,
        )
        cls.permis_add = Permission.objects.get(
            codename="add_advertisement",
            content_type=content_type,
        )
        cls.permis_update = Permission.objects.get(
            codename="change_advertisement",
            content_type=content_type,
        )
        cls.permis_del = Permission.objects.get(
            codename="delete_advertisement",
            content_type=content_type,
        )

    def _test_get_unauthorized(self, url):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={url}")

    def _test_get_not_permis(self, url):
        "Проверка, что пользователь без нужного разрешения не может просмотреть соответствующую страницу."
        self.client.force_login(self.user)
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 403)


class TestAdvertisementListView(BaseAdvertisementTestCase):
    """
    Тесты для представленния AdvertisementList.
    """

    fixtures = ["advertisement.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("ad_campaign:ad_list")

    def test_get_advertisement_list(self):
        "Проверка получения списка рекламных кампаний."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(Advertisement.objects.count(), 2)

    def test_get_advertisement_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_advertisement_list_permis(self):
        "Проверка, что пользователь без разрешения view_advertisement не может просмотреть список рекламных кампаний."
        self._test_get_not_permis(self.url)


class TestAdvertisementCreate(BaseAdvertisementTestCase):
    """
    Тесты для представленния AdvertisementCreate.
    """

    fixtures = ["advertisement.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("ad_campaign:ad_create")

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
            "title": "Test add advertisement",
            "service": 3,
            "promotion_channel": "Test create advertisement",
            "budget": Decimal("500.00"),
        }
        respons = self.client.post(self.url, data=data)
        advertisement = Advertisement.objects.get(title="Test add advertisement")

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(
            respons, reverse("ad_campaign:ad_detail", args=[advertisement.pk])
        )

    def test_get_advertisement_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_advertisement_create_permis(self):
        "Проверка, что пользователь без разрешения add_advertisement не может создать новую рекламную кампанию."
        self._test_get_not_permis(self.url)


class TestAdvertisementDetail(BaseAdvertisementTestCase):
    """
    Тесты для представленния AdvertisementDetail.
    """

    fixtures = ["advertisement.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("ad_campaign:ad_detail", args=[1])

    def test_get_advertisement_detail(self):
        "Проверка получения страницы деталей рекламной кампании."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)
        advertisement = Advertisement.objects.get(pk=1)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "ad_campaign/ads_detail.html")
        self.assertEqual(respons.context["object"], advertisement)

    def test_get_advertisement_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_advertisement_detail_permis(self):
        "Проверка, что пользователь без разрешения view_advertisement не может просмотреть детальную страницу рекламной кампании."
        self._test_get_not_permis(self.url)


class TestAdvertisementUpdate(BaseAdvertisementTestCase):
    """
    Тесты для представленния AdvertisementUpdate.
    """

    fixtures = ["advertisement.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("ad_campaign:ad_update", args=[1])

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
            "title": "Test update",
            "service": 1,
            "promotion_channel": "Test 1",
            "budget": "500.00",
        }
        respons = self.client.post(self.url, data=data)
        advertisement = Advertisement.objects.get(pk=1)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("ad_campaign:ad_detail", args=[1]))
        self.assertEqual(advertisement.title, "Test update")
        self.assertEqual(advertisement.promotion_channel, "Test 1")
        self.assertEqual(advertisement.budget, Decimal("500.00"))

    def test_get_advertisement_update_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_advertisement_update_permis(self):
        "Проверка, что пользователь без разрешения change_advertisement не может изменить рекламную кампанию."
        self._test_get_not_permis(self.url)


class TestAdvertisementDelete(BaseAdvertisementTestCase):
    """
    Тесты для представленния AdvertisementDelete.
    """

    fixtures = ["advertisement.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("ad_campaign:ad_delete", args=[2])

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
        self._test_get_unauthorized(self.url)

    def test_get_advertisement_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_services не может удалить рекламную кампанию."
        self._test_get_not_permis(self.url)
