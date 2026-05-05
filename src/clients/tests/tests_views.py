from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Lead


class BaseLeadTestCase(TestCase):
    """
    Базовый класс для тестов приложения clients.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="pass")
        content_type = ContentType.objects.get_for_model(Lead)
        cls.permis_view = Permission.objects.get(
            codename="view_lead",
            content_type=content_type,
        )
        cls.permis_add = Permission.objects.get(
            codename="add_lead",
            content_type=content_type,
        )
        cls.permis_update = Permission.objects.get(
            codename="change_lead",
            content_type=content_type,
        )
        cls.permis_del = Permission.objects.get(
            codename="delete_lead",
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


class TestLeadList(BaseLeadTestCase):
    """
    Тесты для представленния LeadList.
    """

    fixtures = ["clients.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("clients:clients_list")

    def test_get_lead_list(self):
        "Проверка получения списка потенциальных клиентов."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(Lead.objects.count(), 2)

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения view_lead не может просмотреть список потенциальных клиентов."
        self._test_get_not_permis(self.url)


class TestLeadDetail(BaseLeadTestCase):
    """
    Тесты для представленния LeadList.
    """

    fixtures = ["clients.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("clients:clients_detail", args=[1])

    def test_get_lead_detail(self):
        "Проверка получения страницы деталей потенциального клиента."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)
        lead = Lead.objects.get(pk=1)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_detail.html")
        self.assertEqual(respons.context["object"], lead)

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения view_lead не может просмотреть детали потенциального клиента."
        self._test_get_not_permis(self.url)


class TestLeadCreate(BaseLeadTestCase):
    """
    Тесты для представленния LeadCreate.
    """

    fixtures = ["clients.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("clients:clients_create")

    def test_get_lead_create(self):
        "Проверка получения формы для добавления потенциального клиента."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_create.html")

    def test_post_lead_create(self):
        "Проверка добавления нового потенциального клиента."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "first_name": "Create",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "+79456542656",
            "email": "test@mail.com",
            "advertisement": 3,
        }
        respons = self.client.post(self.url, data=data)
        lead = Lead.objects.get(first_name="Create")

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("clients:clients_detail", args=[lead.pk]))

    def test_get_lead_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_lead_creat_permis(self):
        "Проверка, что пользователь без разрешения add_lead не может добавить нового потенциального клиента."
        self._test_get_not_permis(self.url)


class TestLeadUpdate(BaseLeadTestCase):
    """
    Тесты для представленния LeadUpdate.
    """

    fixtures = ["clients.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("clients:clients_update", args=[1])

    def test_get_lead_update(self):
        "Проверка получения формы для редактирования информации о потенциальном клиенте."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_edit.html")

    def test_post_lead_update(self):
        "Проверка редактирования информации о потенциальном клиенте."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "first_name": "Update",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "+79456542656",
            "email": "test@mail.com",
            "advertisement": 1,
        }
        respons = self.client.post(self.url, data=data)
        lead = Lead.objects.get(pk=1)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("clients:clients_detail", args=[1]))
        self.assertEqual(lead.first_name, "Update")
        self.assertEqual(lead.last_name, "Test Last Name")
        self.assertEqual(lead.patronymic, "Test Patron")
        self.assertEqual(lead.phone, "+79456542656")
        self.assertEqual(lead.email, "test@mail.com")

    def test_get_lead_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_lead_list_permis(self):
        "Проверка, что пользователь без разрешения change_lead не может изменить информацию у потенциального клиента."
        self._test_get_not_permis(self.url)


class TestLeadDelete(BaseLeadTestCase):
    """
    Тесты для представленния LeadDelete.
    """

    fixtures = ["clients.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("clients:clients_delete", args=[2])

    def test_get_lead_delete(self):
        "Проверка получения формы для удаления потенциального клиента."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "clients/leads_delete.html")

    def test_delete_lead(self):
        "Проверка удаления потенциального клиента."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("clients:clients_list"))

    def test_get_lead_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_lead_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_lead не может удалить потенциального клиента."
        self._test_get_not_permis(self.url)
