from django.db import models
from django.utils import timezone
from api.models import Visit
from django.apps import apps


class Consult(models.Model):
    class Meta:
        db_table = "consults"

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(
        "api.CustomUser",
        related_name="doctor_create",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    past_medical_history = models.TextField(blank=True, null=True)
    consultation = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    referred_for = models.TextField(blank=True, null=True)
    referral_notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
