from django.db import models


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    warning_quantity = models.PositiveIntegerField(null=True, blank=True, default=None)
    isCurrentStock = models.BooleanField(blank=False, default=True)
