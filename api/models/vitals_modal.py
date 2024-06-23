from django.db import models
from api.models import Visit


class Vitals(models.Model):
    class Meta:
        db_table = "vitals"

    visit = models.OneToOneField(
        Visit, on_delete=models.SET_NULL, blank=True, null=True
    )
    height = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    systolic = models.IntegerField(null=True)
    diastolic = models.IntegerField(null=True)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    diabetes_mellitus = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    heart_rate = models.IntegerField(null=True)
    urine_test = models.TextField(blank=True, null=True)
    hemocue_count = models.DecimalField(decimal_places=2, max_digits=5)
    blood_glucose = models.DecimalField(decimal_places=2, max_digits=5)
    left_eye_degree = models.TextField(blank=True, null=True)
    right_eye_degree = models.TextField(blank=True, null=True)
    left_eye_pinhole = models.TextField(blank=True, null=True)
    right_eye_pinhole = models.TextField(blank=True, null=True)
    others = models.TextField(blank=True, null=True)
