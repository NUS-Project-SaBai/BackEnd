from django.db import models
from api.models import Patient


class File(models.Model):
    class Meta:
        db_table = "file"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    file_path = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
