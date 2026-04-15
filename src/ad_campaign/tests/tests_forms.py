from decimal import Decimal
from django.test import TestCase

from ..form import AdvertisementForm
from ...services.models import Services


class TestAdvertisementForm(TestCase):
    """
    Тесты для формы AdvertisementForm.
    """

    def test_advertisement_valid_form(self):
        "Тестирование валидной формы ServicesForm."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        data = {
            "title": "test",
            "service": service,
            "promotion_channel": "test form",
            "budget": Decimal("500.00"),
        }
        form = AdvertisementForm(data=data)

        self.assertTrue(form.is_valid())

    def test_advertisement_invalid_title(self):
        "Отправка формы с пустым названием."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        data = {
            "title": "",
            "service": service,
            "promotion_channel": "test form",
            "budget": Decimal("500.00"),
        }
        form = AdvertisementForm(data=data)

        self.assertFalse(form.is_valid())

    def test_advertisement_invalid_service(self):
        "Отправка формы без выбора услуги."
        data = {
            "title": "test",
            "promotion_channel": "test form",
            "budget": Decimal("500.00"),
        }
        form = AdvertisementForm(data=data)

        self.assertFalse(form.is_valid())

    def test_advertisement_invalid_promotion_channel(self):
        "Отправка формы без обозначенного канала продвижения."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        data = {
            "title": "test",
            "service": service,
            "promotion_channel": "",
            "budget": Decimal("500.00"),
        }
        form = AdvertisementForm(data=data)

        self.assertFalse(form.is_valid())

    def test_advertisement_form_invalid_budget(self):
        "Отправка формы с отрицательным бюджетом."
        service = Services.objects.create(
            title="Title Service",
            description="descrip",
            cost=Decimal("500.00"),
        )
        data = {
            "title": "test",
            "service": service,
            "promotion_channel": "test form",
            "budget": Decimal("-500.00"),
        }
        form = AdvertisementForm(data=data)

        self.assertFalse(form.is_valid())
