from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Patient
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
import cloudinary.uploader


class Command(BaseCommand):
    help = "Upload local images to cloudinary"

    def handle(self, *args, **kwargs):
        try:
            patients = Patient.objects.all()
            for patient in patients:
                if patient.offline_picture & patient.is_image_edited:
                    upload_result = cloudinary.uploader.upload(
                        patient.offline_picture.path
                    )
                    patient.is_image_edited = False
                    patient.picture = upload_result["secure_url"].replace(CLOUDINARY_URL + "/image/upload/", "")
                    patient.save()
            self.stdout.write("Pictures uploaded successfully")
        except IntegrityError as e:
            self.stdout.write(f"Something went wrong! Error: {e}")
