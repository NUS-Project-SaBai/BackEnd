from django.db import models
from django.utils import timezone
from api.models import Patient


class Visit(models.Model):
    class Meta:
        db_table = "visits"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)
