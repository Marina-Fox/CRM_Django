import tempfile

from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Contracts


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


class BaseContractsTestCase(TestCase):
    """
    Базовый класс для тестов приложения contracts.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="pass")
        content_type = ContentType.objects.get_for_model(Contracts)
        cls.permis_view = Permission.objects.get(
            codename="view_contracts",
            content_type=content_type,
        )
        cls.permis_add = Permission.objects.get(
            codename="add_contracts",
            content_type=content_type,
        )
        cls.permis_update = Permission.objects.get(
            codename="change_contracts",
            content_type=content_type,
        )
        cls.permis_del = Permission.objects.get(
            codename="delete_contracts",
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


class TestContractsList(BaseContractsTestCase):
    """
    Тесты для представленния ContractsList.
    """

    fixtures = ["contracts.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.url = reverse("contracts:contracts_list")

    def test_get_contracts_list(self):
        "Проверка получения списка контрактов."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertEqual(Contracts.objects.count(), 2)

    def test_get_contracts_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_contracts_list_permis(self):
        "Проверка, что пользователь без разрешения view_contracts не может просмотреть список контрактов."
        self._test_get_not_permis(self.url)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsDetail(BaseContractsTestCase):
    """
    Тесты для представленния ContractsDetail.
    """

    fixtures = ["contracts.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.contract = Contracts.objects.get(pk=1)
        file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        cls.contract.file_doc.save("test 1.pdf", file_contr)
        cls.url = reverse("contracts:contracts_detail", args=[1])

    def test_get_contracts_detail(self):
        "Проверка получения страницы деталей контракта."
        self.user.user_permissions.add(self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "contracts/contracts_detail.html")
        self.assertEqual(respons.context["object"], self.contract)

    def test_get_contracts_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_contracts_detail_permis(self):
        "Проверка, что пользователь без разрешения view_contracts не может просмотреть детальную страницу контракта."
        self._test_get_not_permis(self.url)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsCreate(BaseContractsTestCase):
    """
    Тесты для представленния ContractsCreate.
    """

    fixtures = ["contracts.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        cls.end_date = date.today() + timedelta(days=30)
        cls.url = reverse("contracts:contracts_create")

    def test_get_contracts_create(self):
        "Проверка получения формы для добавления нового контракта."
        self.user.user_permissions.add(self.permis_add)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "contracts/contracts_create.html")

    def test_post_contracts_create(self):
        "Проверка добавления нового контракта."
        self.user.user_permissions.add(self.permis_add, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Contr Create",
            "service": 3,
            "file_doc": self.file_contr,
            "end_date": self.end_date,
            "cost": Decimal("500000.00"),
        }
        respons = self.client.post(self.url, data=data)
        contract = Contracts.objects.get(title="Test Contr Create")

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(
            respons, reverse("contracts:contracts_detail", args=[contract.pk])
        )

    def test_get_contracts_create_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_contracts_create_permis(self):
        "Проверка, что пользователь без разрешения add_contracts не может добавить новый контракт."
        self._test_get_not_permis(self.url)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsUpdate(BaseContractsTestCase):
    """
    Тестирование представления ContractsUptade.
    """

    fixtures = ["contracts.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.contract = Contracts.objects.get(pk=1)
        file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        cls.contract.file_doc.save("test 1.pdf", file_contr)
        cls.url = reverse("contracts:contracts_update", args=[1])

    def test_get_contracts_update(self):
        "Проверка получения формы для обновления данных контракта."
        self.user.user_permissions.add(self.permis_update)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "contracts/contracts_edit.html")

    def test_post_contracts_update(self):
        "Проверка внесения изменений в данные контракта."
        self.user.user_permissions.add(self.permis_update, self.permis_view)
        self.client.force_login(self.user)
        data = {
            "title": "Test Contr Update",
            "service": 1,
            "end_date": "2026-09-30",
            "cost": "5000.00",
        }
        respons = self.client.post(self.url, data=data)
        contract = Contracts.objects.get(pk=1)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("contracts:contracts_detail", args=[1]))
        self.assertEqual(contract.title, "Test Contr Update")
        self.assertEqual(contract.cost, Decimal("5000.00"))

    def test_get_contracts_update_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_contracts_update_permis(self):
        "Проверка, что пользователь без разрешения change_contracts не может изменить данные контракта."
        self._test_get_not_permis(self.url)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsDelete(BaseContractsTestCase):
    """
    Тестирование представления ContractsDelete.
    """

    fixtures = ["contracts.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        cls.contract = Contracts.objects.get(pk=2)
        cls.contract.file_doc.save("test 1.pdf", file_contr)
        cls.url = reverse("contracts:contracts_delete", args=[2])

    def test_get_contracts_delete(self):
        "Проверка получения формы для удаления контракта."
        self.user.user_permissions.add(self.permis_del)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "contracts/contracts_delete.html")

    def test_delete_contracts(self):
        "Проверка удаления контракта."
        self.user.user_permissions.add(self.permis_del, self.permis_view)
        self.client.force_login(self.user)
        respons = self.client.delete(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, reverse("contracts:contracts_list"))

    def test_get_contracts_delete_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        self._test_get_unauthorized(self.url)

    def test_get_contracts_delete_permis(self):
        "Проверка, что пользователь без разрешения delete_contracts не может удалить контракт."
        self._test_get_not_permis(self.url)
