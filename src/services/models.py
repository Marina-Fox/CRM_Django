from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Services(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    description = models.TextField(verbose_name="Описание", max_length=1000)
    cost = models.DecimalField(verbose_name="Стоимость", max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    def __str__(self):
        return self.title
