from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Services


class BaseServicesTestCase(TestCase):
    """
    Базовый класс для тестов приложения services.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="pass")
        content_type = ContentType.objects.get_for_model(Services)
        cls.permis_view = Permission.objects.get(
            codename="view_services",
            content_type=content_type,
        )
        cls.permis_add = Permission.objects.get(
            codename="add_services",
            content_type=content_type,
        )
        cls.permis_update = Permission.objects.get(
            codename="change_services",
            content_type=content_type,
        )
        cls.permis_del = Permission.objects.get(
            codename="delete_services",
            content_type=content_type,
        )

    def _test_get_unauthorized(self, url):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/users/login/?next={url}")

    def _test_get_not_permis(self, url):
        "Проверка, что пользователь без нужного разрешения не может просмотреть соответствующую страницу."
        self.client.force_login(self.user)
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 403)


class TestServicesListView(BaseServicesTestCase):
    """
    Тесты для представленния ServicesList.
    """

    fixtures = ["services.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("services:services_list")

    def test_get_services_list(self):
        "Проверка получения списка услуг."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(Services.objects.count(), 2)

    def test_get_services_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_services_list_permis(self):
        "Проверка, что пользователь без разрешения view_services не может просмотреть список услуг."
        self._test_get_not_permis(self.url)


class TestServicesDetailView(BaseServicesTestCase):
    """
    Тесты для представленния ServicesDetail.
    """

    fixtures = ["services.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("services:services_detail", args=[1])

    def test_get_services_detail(self):
        "Проверка получения страницы деталей услуги."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)
        service = Services.objects.get(pk=1)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_detail.html")
        self.assertEqual(respons.context["object"].title, service.title)
        self.assertEqual(respons.context["object"].cost, service.cost)

    def test_get_services_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_services_detail_permis(self):
        "Проверка, что пользователь без разрешения view_services не может просмотреть детальную страницу услуги."
        self._test_get_not_permis(self.url)


class TestServicesCreateView(BaseServicesTestCase):
    """
    Тесты для представленния ServicesCreate.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("services:services_create")

    def test_get_services_create(self):
        "Проверка получения формы для создания услуги."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_create.html")

    def test_post_services_create(self):
        "Проверка создания новой услуги."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Create",
            "description": "Test create",
            "cost": "500.00",
        }
        respons = self.client.post(self.url, data=data)
        service = Services.objects.get(title="Test Create")

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(
            respons, reverse("services:services_detail", args=[service.pk])
        )

    def test_get_services_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_services_create_permis(self):
        "Проверка, что пользователь без разрешения add_services не может создать новую услугу."
        self._test_get_not_permis(self.url)


class TestServicesUpdateView(BaseServicesTestCase):
    """
    Тесты для представленния ServicesUpdate.
    """

    fixtures = ["services.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("services:services_update", args=[1])

    def test_get_services_update(self):
        "Проверка получения формы для обновления услуги."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_edit.html")

    def test_post_services_update(self):
        "Проверка внесения изменений в услугу."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Update",
            "description": "Test update",
            "cost": "50.00",
        }
        respons = self.client.post(self.url, data=data)
        service = Services.objects.get(pk=1)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("services:services_detail", args=[1]))
        self.assertEqual(service.title, "Test Update")
        self.assertEqual(service.description, "Test update")
        self.assertEqual(service.cost, Decimal("50.00"))

    def test_get_services_update_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_services_update_permis(self):
        "Проверка, что пользователь без разрешения change_services не может изменить услугу."
        self._test_get_not_permis(self.url)


class TestServicesDeleteView(BaseServicesTestCase):
    """
    Тесты для представленния ServicesDelete.
    """

    fixtures = ["services.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("services:services_delete", args=[2])

    def test_get_services_delete(self):
        "Проверка получения формы для удаления услуги."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "services/services_delete.html")

    def test_delete_services(self):
        "Проверка удаления услуги."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("services:services_list"))

    def test_get_services_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_services_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_services не может удалить услугу."
        self._test_get_not_permis(self.url)
