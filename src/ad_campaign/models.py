from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from ..services.models import Services


# Create your models here.
class Advertisement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    service = models.ForeignKey(
        Services, verbose_name="Услуга", on_delete=models.CASCADE
    )
    promotion_channel = models.CharField(
        verbose_name="Канал продвижения", max_length=200
    )
    budget = models.DecimalField(
        verbose_name="Бюджет",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        default=Decimal("0.00")
    )

    class Meta:
        verbose_name = "рекламная кампания"
        verbose_name_plural = "рекламные кампании"

    def __str__(self):
        return self.title
