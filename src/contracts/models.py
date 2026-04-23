from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

from ..services.models import Services

# Create your models here.
class Contracts(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    service = models.ForeignKey(
        Services,
        verbose_name="Услуга",
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    file_doc = models.FileField(upload_to="contracts/%Y/%m/%d/", verbose_name="Файл контракта")
    start_date = models.DateField(verbose_name="Дата заключения", default=timezone.now())
    end_date = models.DateField(verbose_name="Окончание действия")
    cost = models.DecimalField(
        verbose_name="Стоимость",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    def __str__(self):
        return f"{self.title} {self.service.title}"
