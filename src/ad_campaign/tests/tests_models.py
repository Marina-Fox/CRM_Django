from django.test import TestCase
from decimal import Decimal

from ..models import Advertisement
from ...services.models import Services
from django.core.exceptions import ValidationError

# Create your tests here.
class TestAdvertisementModel(TestCase):
    """
    Тесты для модели Advertisement.
    """
    def test_model_advertisement_creation(self):
        "Проверка создания модели Advertisement."
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

        self.assertTrue(isinstance(advertisement, Advertisement))
        self.assertEqual(advertisement.title, "Title")
        self.assertEqual(str(advertisement), "Title")
        self.assertEqual(advertisement.service.title, service.title)
        self.assertEqual(advertisement.promotion_channel, "Интернет")
        self.assertEqual(advertisement.budget, Decimal("10000.00"))

    def test_model_advertisement_title_req(self):
        "Название не должно быть пустым."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )
        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_titl_max_length(self):
        "Название не должно превышать 200 символов."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="T" * 201,
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_servise(self):
        "Реклама должна быть связана с услугой"
        advertisement = Advertisement(
            title="Title",
            promotion_channel="Интернет",
            budget=Decimal("10000.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_promotion_channel_req(self):
        "Канал продвижения должен быть обозначен."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="Title",
            service=service,
            promotion_channel="",
            budget=Decimal("10000.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_promotion_channel_max_length(self):
        "Канал продвижения не должен превышать 200 символов."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="Title",
            service=service,
            promotion_channel="t" * 201,
            budget=Decimal("10000.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_budget_zero(self):
        "Бюджет должен быть бальше 0."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("0.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_budget_max_digits(self):
        "Суммарное количество цифр в стоимости (целая и дробная части) не может превышать 10."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("500000000.00"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()

    def test_model_advertisement_budget_decimal_places(self):
        "Количество знаков после десятичной точки в стоимости не может превышать 2."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        advertisement = Advertisement(
            title="Title",
            service=service,
            promotion_channel="Интернет",
            budget=Decimal("500.003"),
        )

        with self.assertRaises(ValidationError):
            advertisement.full_clean()
