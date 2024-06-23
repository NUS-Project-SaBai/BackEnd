from django.db import models


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
