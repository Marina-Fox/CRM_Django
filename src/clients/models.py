from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

from ..ad_campaign.models import Advertisement


# Create your models here.
class Lead(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    patronymic = models.CharField(
        verbose_name="Отчество", max_length=50, blank=True, null=True
    )
    phone = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Email", max_length=50)
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name="Рекламная кампания",
        related_name = "leads",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
    )
    contracts = models.ManyToManyField(
        "contracts.Contracts", verbose_name="Контракты", through="customers.Customers"
    )

    class Meta:
        verbose_name = "потенциальный клиент"
        verbose_name_plural = "потенциальные клиенты"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
