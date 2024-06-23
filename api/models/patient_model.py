from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Patient(models.Model):
    class Meta:
        db_table = "patients"

    village_prefix = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateTimeField(default=timezone.now)
    drug_allergy = models.TextField(default="None")
    face_encodings = models.CharField(max_length=3000, blank=True, null=True)
    picture = CloudinaryField("image")
