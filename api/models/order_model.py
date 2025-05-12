from django.db import models
from api.models import Consult, MedicationReview


class Order(models.Model):
    class Meta:
        db_table = "order"

    consult = models.ForeignKey(
        Consult,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="prescriptions",
    )
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    medication_review = models.ForeignKey(
        MedicationReview,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order",
    )
