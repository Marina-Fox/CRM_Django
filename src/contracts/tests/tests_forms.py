import tempfile

from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..form import ContractsForm
from ...services.models import Services


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestContractsForm(TestCase):
    """
    Тесты для формы ContractsForm.
    """

    def setUp(self) -> None:
        self.service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        self.file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        self.end_date = date.today() + timedelta(days=30)

    def test_contracts_valid_form(self):
        "Тестирование валидной формы."
        data = {
            "title": "Test Contr 1",
            "service": self.service.pk,
            "end_date": self.end_date,
            "cost": Decimal("500000.00"),
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertTrue(form.is_valid())

    def test_contracts_invalid_title(self):
        "Отправка формы с пустым названием."
        data = {
            "title": "",
            "service": self.service.pk,
            "end_date": self.end_date,
            "cost": Decimal("500000.00"),
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertFalse(form.is_valid())

    def test_contracts_invalid_service(self):
        "Отправка формы без выбора услуги."
        data = {
            "title": "Test Contr 1",
            "end_date": self.end_date,
            "cost": Decimal("500000.00"),
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertFalse(form.is_valid())

    def test_contracts_invalid_file_doc(self):
        "Отправка формы без файла."
        data = {
            "title": "Test Contr 1",
            "service": self.service.pk,
            "end_date": self.end_date,
            "cost": Decimal("500000.00"),
        }
        form = ContractsForm(data=data)

        self.assertFalse(form.is_valid())

    def test_contracts_invalid_end_date(self):
        "Отправка формы без указания даты окончания действия контракта."
        data = {
            "title": "Test Contr 1",
            "service": self.service.pk,
            "cost": Decimal("500000.00"),
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertFalse(form.is_valid())

    def test_contracts_invalid_cost_none(self):
        "Отправка формы без указания стоимости."
        data = {
            "title": "Test Contr 1",
            "service": self.service.pk,
            "end_date": self.end_date,
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertFalse(form.is_valid())

    def test_contracts_invalid_cost_negative(self):
        "Отправка формы с отрицательной стоимостью."
        data = {
            "title": "Test Contr 1",
            "service": self.service.pk,
            "end_date": self.end_date,
            "cost": Decimal("-500000.00"),
        }
        files = {
            "file_doc": self.file_contr,
        }
        form = ContractsForm(data=data, files=files)

        self.assertFalse(form.is_valid())
