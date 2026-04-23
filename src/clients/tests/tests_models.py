from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Lead
from ...ad_campaign.models import Advertisement
from ...services.models import Services


class TestLeadModel(TestCase):
    """
    Тесты для модели Lead.
    """

    def test_model_lead_creation(self):
        "Проверка создания модели Lead."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead.objects.create(
            first_name="Петр",
            last_name="Петрович",
            patronymic="",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        self.assertTrue(isinstance(lead, Lead))
        self.assertEqual(lead.first_name, "Петр")
        self.assertEqual(lead.last_name, "Петрович")
        self.assertEqual(str(lead), "Петр Петрович")
        self.assertEqual(lead.phone, "89091234567")
        self.assertEqual(lead.email, "exampl@mail.com")
        self.assertEqual(lead.advertisement.title, advertisement.title)

    def test_model_lead_first_name_req(self):
        "Поле для имени не может быть пустым."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="",
            last_name="Петрович",
            patronymic="Петров",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_first_name_max_length(self):
        "Имя не должно превышать 50 символов."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="п" * 51,
            last_name="Петрович",
            patronymic="Петров",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_last_name_req(self):
        "Поле для фамилии не может быть пустым."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="Петр",
            last_name="",
            patronymic="Петров",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_last_name_max_length(self):
        "Фамилия не должна превышать 50 символов."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="Петр",
            last_name="g" * 51,
            patronymic="Петров",
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_patronymic_max_length(self):
        "Отчество не должна превышать 50 символов."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="Петр",
            last_name="Петрович",
            patronymic="п" * 51,
            phone="89091234567",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_phone_req(self):
        "Поле для телефона не может быть пустым."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="Петр",
            last_name="Петрович",
            patronymic="Петров",
            phone="",
            email="exampl@mail.com",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()

    def test_model_lead_email_req(self):
        "Поле для почты не может быть пустым."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement.objects.create(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        lead = Lead(
            first_name="Петр",
            last_name="Петрович",
            patronymic="Петров",
            phone="89091234567",
            email="",
            advertisement=advertisement,
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()
