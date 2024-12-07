from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Medication
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
from django.conf import settings
import os
import psycopg2
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = "Get image from cloudinary to offline"

    def handle(self, *args, **kwargs):
        try:
            oriMedication = Medication.objects.all()

            for medication in oriMedication:
                medication.quantity = 0
                medication.save()


        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Close the cursor and connection
            pass