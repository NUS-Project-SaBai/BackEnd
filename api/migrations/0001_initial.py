# Generated by Django 5.0.6 on 2024-09-17 18:20

import cloudinary.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="JWKS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("jwks", models.JSONField()),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Medication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("medicine_name", models.CharField(max_length=255)),
                ("quantity", models.IntegerField(default=0)),
                ("notes", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "medication",
            },
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("village_prefix", models.CharField(max_length=5)),
                ("name", models.CharField(max_length=255)),
                (
                    "identification_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("contact_no", models.CharField(blank=True, max_length=255, null=True)),
                ("gender", models.CharField(max_length=11)),
                (
                    "date_of_birth",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("poor", models.CharField(default="No", max_length=3)),
                ("bs2", models.CharField(default="No", max_length=3)),
                ("drug_allergy", models.TextField(default="None")),
                (
                    "face_encodings",
                    models.CharField(blank=True, max_length=3000, null=True),
                ),
                (
                    "picture",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
            ],
            options={
                "db_table": "patients",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("auth0_id", models.CharField(max_length=255)),
                ("nickname", models.CharField(max_length=255)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Consult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("past_medical_history", models.TextField(blank=True, null=True)),
                ("consultation", models.TextField(blank=True, null=True)),
                ("plan", models.TextField(blank=True, null=True)),
                ("referred_for", models.TextField(blank=True, null=True)),
                ("referral_notes", models.TextField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="doctor_create",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "consults",
            },
        ),
        migrations.CreateModel(
            name="Diagnosis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("details", models.TextField(blank=True, null=True)),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "consult",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.consult",
                    ),
                ),
            ],
            options={
                "db_table": "diagnosis",
            },
        ),
        migrations.CreateModel(
            name="MedicationReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity_changed", models.IntegerField(default=0)),
                ("quantity_remaining", models.IntegerField(default=0)),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("APPROVED", "Approved"),
                            ("PENDING", "Pending"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=255,
                    ),
                ),
                (
                    "approval",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approval_create_medication_review",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.medication",
                    ),
                ),
            ],
            options={
                "db_table": "medication_review",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                ("remarks", models.TextField(blank=True, null=True)),
                (
                    "consult",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="prescriptions",
                        to="api.consult",
                    ),
                ),
                (
                    "medication_review",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order",
                        to="api.medicationreview",
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_path", models.CharField(max_length=255, null=True)),
                (
                    "offline_file",
                    models.FileField(null=True, upload_to="offline_files/"),
                ),
                ("file_name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.patient",
                    ),
                ),
            ],
            options={
                "db_table": "file",
            },
        ),
        migrations.CreateModel(
            name="Visit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("status", models.CharField(max_length=100)),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.patient",
                    ),
                ),
            ],
            options={
                "db_table": "visits",
            },
        ),
        migrations.AddField(
            model_name="consult",
            name="visit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.visit",
            ),
        ),
        migrations.CreateModel(
            name="Vitals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "temperature",
                    models.DecimalField(decimal_places=2, max_digits=5, null=True),
                ),
                (
                    "systolic",
                    models.DecimalField(
                        blank=True, decimal_places=0, max_digits=3, null=True
                    ),
                ),
                (
                    "diastolic",
                    models.DecimalField(
                        blank=True, decimal_places=0, max_digits=3, null=True
                    ),
                ),
                (
                    "heart_rate",
                    models.DecimalField(
                        blank=True, decimal_places=0, max_digits=3, null=True
                    ),
                ),
                (
                    "hemocue_count",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "diabetes_mellitus",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("urine_test", models.TextField(blank=True, null=True)),
                (
                    "blood_glucose",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("left_eye_degree", models.TextField(blank=True, null=True)),
                ("right_eye_degree", models.TextField(blank=True, null=True)),
                ("left_eye_pinhole", models.TextField(blank=True, null=True)),
                ("right_eye_pinhole", models.TextField(blank=True, null=True)),
                ("gross_motor", models.TextField(blank=True, null=True)),
                ("red_reflex", models.TextField(blank=True, null=True)),
                ("scoliosis", models.TextField(blank=True, null=True)),
                ("pallor", models.TextField(blank=True, null=True)),
                ("oral_cavity", models.TextField(blank=True, null=True)),
                ("heart", models.TextField(blank=True, null=True)),
                ("abdomen", models.TextField(blank=True, null=True)),
                ("lungs", models.TextField(blank=True, null=True)),
                ("hernial_orifices", models.TextField(blank=True, null=True)),
                (
                    "pubarche",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("pubarche_age", models.IntegerField(blank=True, null=True)),
                (
                    "thelarche",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("thelarche_age", models.IntegerField(blank=True, null=True)),
                (
                    "menarche",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("menarche_age", models.IntegerField(blank=True, null=True)),
                (
                    "voice_change",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("voice_change_age", models.IntegerField(blank=True, null=True)),
                (
                    "testicular_growth",
                    models.TextField(
                        blank=True, default="Haven't Asked / Not Applicable", null=True
                    ),
                ),
                ("testicular_growth_age", models.IntegerField(blank=True, null=True)),
                ("others", models.TextField(blank=True, null=True)),
                (
                    "visit",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.visit",
                    ),
                ),
            ],
            options={
                "db_table": "vitals",
            },
        ),
    ]
