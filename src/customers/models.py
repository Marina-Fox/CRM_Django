from django.db import models


# Create your models here.
class Customers(models.Model):
    lead = models.ForeignKey(
        "clients.Lead", verbose_name="Клиент", related_name="customers", on_delete=models.PROTECT
    )
    contract = models.ForeignKey(
        "contracts.Contracts", verbose_name="Контракт", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "активный клиент"
        verbose_name_plural = "активные клиенты"
        unique_together = ["lead", "contract"]
