from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Customers


class BaseCustomersTestCase(TestCase):
    """
    Базовый класс для тестов приложения customers.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="pass")
        content_type = ContentType.objects.get_for_model(Customers)
        cls.permis_view = Permission.objects.get(
            codename="view_customers",
            content_type=content_type,
        )
        cls.permis_add = Permission.objects.get(
            codename="add_customers",
            content_type=content_type,
        )
        cls.permis_update = Permission.objects.get(
            codename="change_customers",
            content_type=content_type,
        )
        cls.permis_del = Permission.objects.get(
            codename="delete_customers",
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


class TestCustomersList(BaseCustomersTestCase):
    """
    Тесты для представленния CustomersList.
    """

    fixtures = ["customers.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("customers:customers_list")

    def test_get_customers_list(self):
        "Проверка получения списка активных клиентов."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(Customers.objects.count(), 2)

    def test_get_customers_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_customers_list_permis(self):
        "Проверка, что пользователь без разрешения view_customers не может просмотреть список активных клиентов."
        self._test_get_not_permis(self.url)


class TestCustomersDetail(BaseCustomersTestCase):
    """
    Тесты для представленния CustomersDetail.
    """

    fixtures = ["customers.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("customers:customers_detail", args=[1])

    def test_get_customers_detail(self):
        "Проверка получения страницы деталей активного клиента."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)
        customer = Customers.objects.get(pk=1)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "customers/customers_detail.html")
        self.assertEqual(respons.context["object"], customer)

    def test_get_customers_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_customers_detail_permis(self):
        "Проверка, что пользователь без разрешения view_customers не может просмотреть детальную страницу активного клиента."
        self._test_get_not_permis(self.url)


class TestCustomersCreate(BaseCustomersTestCase):
    """
    Тесты для представленния CustomersCreate.
    """

    fixtures = ["customers.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("customers:customers_create")

    def test_get_customers_create(self):
        "Проверка получения формы для добавления активного клиента."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "customers/customers_create.html")

    def test_post_customers_create(self):
        "Проверка добавления нового активного клиента."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "lead": 3,
            "contract": 3,
        }
        respons = self.client.post(self.url, data=data)
        customer = Customers.objects.get(lead=3)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(
            respons, reverse("customers:customers_detail", args=[customer.pk])
        )

    def test_get_customers_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_customers_creat_permis(self):
        "Проверка, что пользователь без разрешения add_customers не может добавить нового активного клиента."
        self._test_get_not_permis(self.url)


class TestCustomersUptade(BaseCustomersTestCase):
    """
    Тесты для представленния CustomersUptade.
    """

    fixtures = ["customers.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("customers:customers_update", args=[1])

    def test_get_customers_update(self):
        "Проверка получения формы для редактирования информации об активном клиенте."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "customers/customers_edit.html")

    def test_post_customers_update(self):
        "Проверка редактирования информации об активном клиенте."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "lead": 1,
            "contract": 3,
        }
        respons = self.client.post(self.url, data=data)
        customer = Customers.objects.get(pk=1)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("customers:customers_detail", args=[1]))
        self.assertEqual(customer.lead.pk, 1)
        self.assertEqual(customer.contract.pk, 3)

    def test_get_customers_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_customers_list_permis(self):
        "Проверка, что пользователь без разрешения change_customers не может изменить информацию у активного клиента."
        self._test_get_not_permis(self.url)


class TestCustomersDelete(BaseCustomersTestCase):
    """
    Тесты для представленния CustomersDelete.
    """

    fixtures = ["customers.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("customers:customers_delete", args=[2])

    def test_get_customers_delete(self):
        "Проверка получения формы для удаления активного клиента."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "customers/customers_delete.html")

    def test_delete_customers(self):
        "Проверка удаления активного клиента."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("customers:customers_list"))

    def test_get_customers_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_customers_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_customers не может удалить активного клиента."
        self._test_get_not_permis(self.url)
