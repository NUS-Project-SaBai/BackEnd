from django.db import models
from api.models import Consult, Medication


class Order(models.Model):
    class Meta:
        db_table = "order"

    medicine = models.ForeignKey(
        Medication, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, blank=True)
    consult = models.ForeignKey(
        Consult,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="prescriptions",
    )
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=255)
