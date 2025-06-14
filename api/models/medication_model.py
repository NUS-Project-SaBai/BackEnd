from django.db import models


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=100, unique=True, blank=True, null=True)
