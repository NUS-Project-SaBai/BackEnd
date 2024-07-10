from django.db import models
from api.models import Patient
from django.utils import timezone


class MedicationHistory(models.Model):
    class Meta:
        db_table = "medication_history"

    doctor = models.ForeignKey(
        'api.CustomUser',
        related_name="doctor_create_medication_history",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    quantity_changed = models.IntegerField(default=0)
    quantity_remaining = models.IntegerField(default=0)
    medicine = models.ForeignKey(
        'api.Medication', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
