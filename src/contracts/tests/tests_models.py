import tempfile
import os

from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from ..models import Contracts
from ...services.models import Services


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsModel(TestCase):
    """
    Тесты для модели Contracts.
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

    def test_model_contracts_creation(self):
        "Проверка создания модели Contracts."
        contract = Contracts.objects.create(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )

        self.assertTrue(isinstance(contract, Contracts))
        self.assertEqual(contract.title, "Test Contr")
        self.assertEqual(str(contract), "Test Contr Title Service")
        self.assertEqual(contract.service.title, self.service.title)
        self.assertEqual(contract.end_date, self.end_date)
        self.assertEqual(contract.cost, Decimal("500000.00"))

        file_path = os.path.join(TEMP_MEDIA_ROOT, contract.file_doc.name)

        self.assertTrue(os.path.exists(file_path))

    def test_model_contracts_title_req(self):
        "Название не должно быть пустым."
        contract = Contracts(
            title="",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_title_max_length(self):
        "Название не должно превышать 200 символов."
        contract = Contracts(
            title="r" * 201,
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_servise_req(self):
        "Контракт должн быть связан с услугой."
        contract = Contracts(
            title="Test Contr",
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_file_doc_req(self):
        "Должен быть прикреплен файл контракта."
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            end_date=self.end_date,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_end_date_req(self):
        "Должна быть указана дата окончания действия контракта."
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_end_date_future(self):
        "Дата окончания действия контракта должна быть не раньше даты заключения контракта."
        date_end = date.today() - timedelta(days=30)
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=date_end,
            cost=Decimal("500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_cost_zero(self):
        "Стоимость должна быть бальше 0."
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("-500000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_cost_max_digits(self):
        "Суммарное количество цифр в стоимости (целая и дробная части) не может превышать 12."
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("50000000000.00"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()

    def test_model_contracts_cost_decimal_places(self):
        "Количество знаков после десятичной точки в стоимости не может превышать 2."
        contract = Contracts(
            title="Test Contr",
            service=self.service,
            file_doc=self.file_contr,
            end_date=self.end_date,
            cost=Decimal("500000.001"),
        )

        with self.assertRaises(ValidationError):
            contract.full_clean()
