# Generated by Django 5.0.6 on 2024-09-11 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_vitals_gross_motor_vitals_heart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitals',
            name='abdomen',
            field=models.TextField(blank=True, null=True),
        ),
    ]
