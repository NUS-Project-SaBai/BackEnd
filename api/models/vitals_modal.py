from django.db import models
from api.models import Visit


class Vitals(models.Model):
    class Meta:
        db_table = "vitals"

    visit = models.OneToOneField(
        Visit, on_delete=models.SET_NULL, blank=True, null=True
    )
    height = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    systolic = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )
    diastolic = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )
    temperature = models.DecimalField(decimal_places=2, max_digits=5, null=True)
    diabetes_mellitus = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    heart_rate = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )
    urine_test = models.TextField(blank=True, null=True)
    hemocue_count = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True
    )
    blood_glucose = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True
    )
    left_eye_degree = models.TextField(blank=True, null=True)
    right_eye_degree = models.TextField(blank=True, null=True)
    left_eye_pinhole = models.TextField(blank=True, null=True)
    right_eye_pinhole = models.TextField(blank=True, null=True)
    others = models.TextField(blank=True, null=True)
