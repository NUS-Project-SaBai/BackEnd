from django.db import models
from api.models import Consult


class Diagnosis(models.Model):
    class Meta:
        db_table = "diagnosis"

    consult = models.ForeignKey(
        Consult, on_delete=models.SET_NULL, blank=True, null=True
    )
    details = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
