from django.db import models


# Create your models here.
class Customers(models.Model):
    lead = models.ForeignKey(
        "clients.Lead", verbose_name="Клиент", on_delete=models.PROTECT
    )
    contract = models.ForeignKey(
        "contracts.Contracts", verbose_name="Контракт", on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ["lead", "contract"]
