import tempfile

from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from ..models import Contracts
from ...services.models import Services


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsList(TestCase):
    """
    Тесты для представленния ContractsList.
    """

    def setUp(self) -> None:
        self.service_1 = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.file_contr_1 = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        self.end_date_1 = date.today() + timedelta(days=30)
        self.contract_1 = Contracts.objects.create(
            title="Test Contr 1",
            service=self.service_1,
            file_doc=self.file_contr_1,
            end_date=self.end_date_1,
            cost=Decimal("500000.00"),
        )
        self.service_2 = Services.objects.create(
            title="Title 2",
            description="descrip 2",
            cost=Decimal("1500.00"),
        )
        self.file_contr_2 = SimpleUploadedFile(
            name="test 2.pdf",
            content=b"test_contract 2",
            content_type="application/pdf",
        )
        self.end_date_2 = date.today() + timedelta(days=10)
        self.contract_2 = Contracts.objects.create(
            title="Test Contr 1",
            service=self.service_2,
            file_doc=self.file_contr_2,
            end_date=self.end_date_2,
            cost=Decimal("5000000.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Contracts)
        self.permis = Permission.objects.get(
            codename="view_contracts",
            content_type=con_type,
        )
        self.url = reverse("contracts:contracts_list")


    def test_get_contracts_list(self):
        "Проверка получения списка контрактов."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertQuerySetEqual(
            respons.context["contracts"],
            [self.contract_1, self.contract_2],
            ordered=False,
        )

    def test_get_advertisement_list_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_list_permis(self):
        "Проверка, что пользователь без разрешения view_contracts не может просмотреть список контрактов."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)


class TestContractsDetail(TestCase):
    """
    Тесты для представленния ContractsDetail.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        self.end_date = date.today() + timedelta(days=30)
        self.contract = Contracts.objects.create(
            title="Test Contr 1",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )
        self.user = User.objects.create_user(username="test_user", password="pass")
        con_type = ContentType.objects.get_for_model(Contracts)
        self.permis = Permission.objects.get(
            codename="view_contracts",
            content_type=con_type,
        )
        self.url = reverse("contracts:contracts_detail", args=[self.contract.pk])

    def test_get_contracts_detail(self):
        "Проверка получения страницы деталей контракта."
        self.user.user_permissions.add(self.permis)
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, "contracts/contracts_detail.html")
        self.assertEqual(respons.context["object"], self.contract)

    def test_get_advertisement_detail_unauthorized(self):
        "Проверка перенаправления пользователя на страницу входа."
        respons = self.client.get(self.url)
        self.assertEqual(respons.status_code, 302)
        self.assertRedirects(respons, f"/admin/login/?next={self.url}")

    def test_get_advertisement_detail_permis(self):
        "Проверка, что пользователь без разрешения view_contracts не может просмотреть детальную страницу контракта."
        self.client.force_login(self.user)
        respons = self.client.get(self.url)

        self.assertEqual(respons.status_code, 403)
