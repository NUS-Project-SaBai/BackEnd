# Generated by Django 5.0.6 on 2024-09-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_vitals_abdomen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitals',
            name='gross_motor',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='menarche',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='pallor',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='pubarche',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='red_reflex',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vitals',
            name='thelarche',
            field=models.TextField(blank=True, null=True),
        ),
    ]
