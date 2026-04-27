from datetime import date
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

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
    file_doc = models.FileField(
        upload_to="contracts/%Y/%m/%d/", verbose_name="Файл контракта"
    )
    start_date = models.DateField(verbose_name="Дата заключения", default=date.today)
    end_date = models.DateField(verbose_name="Окончание действия")
    cost = models.DecimalField(
        verbose_name="Стоимость",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    def __str__(self):
        return f"{self.title} {self.service.title}"

    def clean(self) -> None:
        "Валидация: end_date > start_date."
        super().clean()
        if not self.end_date:
            raise ValidationError(
                {"end_date": "Дата окончания действия контракта должна быть указана."}
            )
        elif self.end_date <= self.start_date:
            raise ValidationError(
                {
                    "end_date": "Дата окончания не может быть раньше даты заключения контракта."
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
