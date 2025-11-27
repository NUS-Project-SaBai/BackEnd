from django.db import models
from api.models import Patient


class File(models.Model):
    class Meta:
        db_table = "file"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    file_path = models.CharField(max_length=255, null=True)
    offline_file = models.FileField(upload_to="offline_files/", null=True)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, db_default="")
    is_deleted = models.BooleanField(default=False)
