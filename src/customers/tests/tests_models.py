import tempfile

from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from ..models import Customers
from ...ad_campaign.models import Advertisement
from ...clients.models import Lead
from ...contracts.models import Contracts
from ...services.models import Services


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestCustomersModel(TestCase):
    """
    Тесты для модели Customers.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.file_contr = SimpleUploadedFile(
            name="test.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        self.end_date = date.today() + timedelta(days=30)
        self.contract = Contracts.objects.create(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )
        self.advertisement = Advertisement.objects.create(
            title="Title",
            service=self.service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        self.lead = Lead.objects.create(
            first_name="Петр",
            last_name="Петрович",
            patronymic="",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=self.advertisement,
        )

    def test_model_customers_creation(self):
        "Проверка создания модели Customers."
        customer = Customers.objects.create(
            lead=self.lead,
            contract=self.contract,
        )

        self.assertTrue(isinstance(customer, Customers))
        self.assertEqual(customer.lead.first_name, self.lead.first_name)
        self.assertEqual(customer.contract.title, self.contract.title)

    def test_model_customers_lead_req(self):
        "Поле lead обязательно для заполнения."
        customer = Customers(
            contract=self.contract,
        )

        with self.assertRaises(ValidationError):
            customer.full_clean()

    def test_model_customers_contract(self):
        "Поле contract обязательно для заполнения."
        customer = Customers(
            lead=self.lead,
        )

        with self.assertRaises(ValidationError):
            customer.full_clean()


# тесты:
# - с 1 клиентом можно заключить несколько контрактов
# - 1 контракт заключен только с 1 клиентом
