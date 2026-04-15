from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError


from ..models import Services


class TestServicesModel(TestCase):
    """
    Тесты для модели Services.
    """

    def test_model_services_creation(self):
        "Проверка создания модели Services."
        service = Services.objects.create(
            title="Title",
            description="descrip",
            cost=Decimal("500.00"),
        )

        self.assertTrue(isinstance(service, Services))
        self.assertEqual(service.title, "Title")
        self.assertEqual(str(service), "Title")
        self.assertEqual(service.description, "descrip")
        self.assertEqual(service.cost, Decimal("500.00"))

    def test_model_service_titl_req(self):
        "Название не должно быть пустым."
        service = Services(
            title="",
            description="descrip",
            cost=Decimal("500.00"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_model_service_titl_max_length(self):
        "Название не должно превышать 200 символов."
        service = Services(
            title="T" * 201,
            description="descrip",
            cost=Decimal("500.00"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_model_service_description_req(self):
        "Описание не должно быть пустым."
        service = Services(
            title="Title",
            description="",
            cost=Decimal("500.00"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_model_service_cost_zero(self):
        "Стоимость должна быть больше 0."
        service = Services(
            title="Title",
            description="descrip",
            cost=Decimal("0.00"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_model_service_cost_max_digits(self):
        "Суммарное количество цифр в стоимости (целая и дробная части) не может превышать 10."
        service = Services(
            title="Title",
            description="descrip",
            cost=Decimal("500000000.00"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_model_service_cost_decimal_places(self):
        "Количество знаков после десятичной точки в стоимости не может превышать 2."
        service = Services(
            title="Title",
            description="descrip",
            cost=Decimal("500.003"),
        )

        with self.assertRaises(ValidationError):
            service.full_clean()
