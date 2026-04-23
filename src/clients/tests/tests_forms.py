from decimal import Decimal
from django.test import TestCase

from ..form import LeadForm
from ...ad_campaign.models import Advertisement
from ...services.models import Services


class TestLeadForm(TestCase):
    """
    Тесты для формы LeadForm.
    """

    def test_lead_valid_form(self):
        "Тестирование валидной формы."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "+79456542656",
            "email": "test@mail.com",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertTrue(form.is_valid())

    def test_lead_invalid_form_first_name(self):
        "ОТправка формы с пустым именем."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "89456542656",
            "email": "test@mail.com",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_lead_invalid_form_last_name(self):
        "Отправка формы без фамилии."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "Test Name",
            "last_name": "",
            "patronymic": "Test Patron",
            "phone": "89456542656",
            "email": "test@mail.com",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_lead_invalid_form_patronymic(self):
        "Отправка формы без отчества."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "",
            "phone": "89456542656",
            "email": "test@mail.com",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_lead_invalid_form_phone(self):
        "Отправка формы с невалидным телефоном."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "89442656",
            "email": "test@mail.com",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_lead_invalid_form_email(self):
        "Отправка формы без почты."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )
        ad_campaign = Advertisement.objects.create(
            title="Test ad camp",
            service=service,
            promotion_channel="Test 1",
            budget=Decimal("500.00"),
        )
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "89456542656",
            "email": "",
            "advertisement": ad_campaign,
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())

    def test_lead_invalid_form_advertisement(self):
        "Отправка формы без указания рекламной кампании."
        data = {
            "first_name": "Test Name",
            "last_name": "Test Last Name",
            "patronymic": "Test Patron",
            "phone": "89456542656",
            "email": "test@mail.com",
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())
