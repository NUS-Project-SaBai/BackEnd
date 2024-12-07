from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Order, MedicationReview
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
            oriMedicationReview = MedicationReview.objects.all()

            for medicationReview in oriMedicationReview:
                medicationReview.order_status = "APPROVED"
                medicationReview.save()


        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Close the cursor and connection
            pass