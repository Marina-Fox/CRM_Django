import tempfile

from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..form import CustomersForm
from ...services.models import Services
from ...contracts.models import Contracts
from ...ad_campaign.models import Advertisement
from ...clients.models import Lead


TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestCustomersForm(TestCase):
    """
    Тесты для формы CustomersForm.
    """

    def setUp(self) -> None:
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        file_contr = SimpleUploadedFile(
            name="test 1.pdf",
            content=b"test_contract",
            content_type="application/pdf",
        )
        end_date = date.today() + timedelta(days=30)
        self.contract = Contracts.objects.create(
            title="Test Contr",
            service=service,
            file_doc=file_contr,
            end_date=end_date,
            cost=Decimal("500000.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        self.lead = Lead.objects.create(
            first_name="Петр",
            last_name="Петрович",
            patronymic="",
            phone="+79091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

    def test_customers_valid_form(self):
        "Тестирование валидной формы."
        data = {"lead": self.lead.pk, "contract": self.contract.pk}
        form = CustomersForm(data=data)

        self.assertTrue(form.is_valid())

    def test_customers_invalid_lead(self):
        "Клиент должен быть указан."
        data = {"contract": self.contract.pk}
        form = CustomersForm(data=data)

        self.assertFalse(form.is_valid())

    def test_customers_invalid_contract(self):
        "Контракт должен быть указан."
        data = {
            "lead": self.lead.pk,
        }
        form = CustomersForm(data=data)

        self.assertFalse(form.is_valid())
