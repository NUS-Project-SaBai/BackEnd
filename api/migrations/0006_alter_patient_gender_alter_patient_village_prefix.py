# Generated by Django 5.0.6 on 2024-07-20 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_patient_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='patient',
            name='village_prefix',
            field=models.CharField(max_length=11),
        ),
    ]
