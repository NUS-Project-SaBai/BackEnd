from django.db import models
from django.utils import timezone


class MedicationReview(models.Model):
    class Meta:
        db_table = "medication_review"

    ORDER_STATUS_CHOICES = [
        ("APPROVED", "Approved"),
        ("PENDING", "Pending"),
        ("CANCELLED", "Cancelled"),
    ]

    approval = models.ForeignKey(
        "api.CustomUser",
        related_name="approval_create_medication_review",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity_changed = models.IntegerField(default=0)
    quantity_remaining = models.IntegerField(default=0)
    medicine = models.ForeignKey("api.Medication", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CHOICES, default="PENDING"
    )
