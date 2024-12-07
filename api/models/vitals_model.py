from django.db import models
from api.models import Visit


class Vitals(models.Model):
    class Meta:
        db_table = "vitals"

    # References
    visit = models.OneToOneField(
        Visit, on_delete=models.SET_NULL, blank=True, null=True
    )

    # General Visit details
    height = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    weight = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    temperature = models.DecimalField(decimal_places=2, max_digits=5, null=True)

    # Heart Vitals
    systolic = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )
    diastolic = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )
    heart_rate = models.DecimalField(
        decimal_places=0, max_digits=3, blank=True, null=True
    )

    # Bio Tests
    hemocue_count = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True
    )
    diabetes_mellitus = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    urine_test = models.TextField(blank=True, null=True)
    blood_glucose_non_fasting = models.DecimalField(
        decimal_places=2, max_digits=5, blank=True, null=True
    )

    # Eye vitals
    left_eye_degree = models.TextField(blank=True, null=True)
    right_eye_degree = models.TextField(blank=True, null=True)
    left_eye_pinhole = models.TextField(blank=True, null=True)
    right_eye_pinhole = models.TextField(blank=True, null=True)

    # Children vitals
    gross_motor = models.TextField(blank=True, null=True)
    red_reflex = models.TextField(blank=True, null=True)
    scoliosis = models.TextField(blank=True, null=True)

    pallor = models.TextField(blank=True, null=True)
    oral_cavity = models.TextField(blank=True, null=True)
    heart = models.TextField(blank=True, null=True)
    abdomen = models.TextField(blank=True, null=True)
    lungs = models.TextField(blank=True, null=True)
    hernial_orifices = models.TextField(blank=True, null=True)

    # Puberty
    pubarche = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    pubarche_age = models.IntegerField(blank=True, null=True)

    # Female Puberty
    thelarche = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    thelarche_age = models.IntegerField(blank=True, null=True)
    menarche = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    menarche_age = models.IntegerField(blank=True, null=True)

    # Male Puberty
    voice_change = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    voice_change_age = models.IntegerField(blank=True, null=True)
    testicular_growth = models.TextField(
        blank=True, null=True, default="Haven't Asked / Not Applicable"
    )
    testicular_growth_age = models.IntegerField(blank=True, null=True)

    # Notes
    others = models.TextField(blank=True, null=True)
