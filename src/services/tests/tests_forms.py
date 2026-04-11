from decimal import Decimal
from django.test import TestCase

from ..form import ServicesForm


class TestServicesForm(TestCase):
    """
    Тесты для формы ServicesForm.
    """
    def test_services_valid_form(self):
        "Тестирование валидной формы ServicesForm."
        data = {
            "title": "Test",
            "description": "Test form",
            "cost": Decimal("500.00"),
        }
        form = ServicesForm(data=data)

        self.assertTrue(form.is_valid())

    def test_services_form_invalid_title(self):
        "Отправка формы с пустым названием."
        data = {
            "title": "",
            "description": "Test form",
            "cost": Decimal("500.00"),
        }
        form = ServicesForm(data=data)

        self.assertFalse(form.is_valid())

    def test_services_form_invalid_description(self):
        "Отправка формы с пустым описанием."
        data = {
            "title": "Test",
            "description": "",
            "cost": Decimal("500.00"),
        }
        form = ServicesForm(data=data)

        self.assertFalse(form.is_valid())

    def test_services_form_invalid_cost(self):
        "Отправка формы с отрицательной стоимостью."
        data = {
            "title": "Test",
            "description": "Test form",
            "cost": Decimal("-500.00"),
        }
        form = ServicesForm(data=data)

        self.assertFalse(form.is_valid())
