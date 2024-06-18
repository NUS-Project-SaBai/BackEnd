from django.db import models
from django.contrib.auth.models import User
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


class Visit(models.Model):
    class Meta:
        db_table = "visits"

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100)


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


class Consult(models.Model):
    class Meta:
        db_table = "consults"

    visit = models.OneToOneField(
        Visit, on_delete=models.SET_NULL, blank=True, null=True
    )
    date = models.DateTimeField(default=timezone.now)
    doctor = models.ForeignKey(
        User,
        related_name="doctor_create",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    past_medical_history = models.TextField(blank=True, null=True)
    consultation = models.TextField(blank=True, null=True)
    plan = models.TextField(blank=True, null=True)
    referred_for = models.TextField(blank=True, null=True)
    referral_notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class Diagnosis(models.Model):
    class Meta:
        db_table = "diagnosis"

    consult = models.ForeignKey(
        Consult, on_delete=models.SET_NULL, blank=True, null=True
    )
    details = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)


class Medication(models.Model):
    class Meta:
        db_table = "medication"

    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class Order(models.Model):
    class Meta:
        db_table = "order"

    medicine = models.ForeignKey(
        Medication, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, blank=True)
    consult = models.ForeignKey(
        Consult, on_delete=models.SET_NULL, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    order_status = models.CharField(max_length=255)
