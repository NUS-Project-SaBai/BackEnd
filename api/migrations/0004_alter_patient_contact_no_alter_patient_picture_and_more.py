# Generated by Django 5.0.6 on 2024-07-20 06:31

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_patient_name_alter_patient_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='contact_no',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='patient',
            name='picture',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='village_prefix',
            field=models.CharField(max_length=5),
        ),
    ]
