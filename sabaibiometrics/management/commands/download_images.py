from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Patient
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL


class Command(BaseCommand):
    help = "Get image from cloudinary to offline"

    def handle(self, *args, **kwargs):
        try:
            patients = Patient.objects.all()
            for patient in patients:
                if patient.picture and patient.is_image_edited: 
                    response = requests.get(f"{CLOUDINARY_URL}/{patient.picture}")
                    if response.status_code == 200:
                        # Create a ContentFile from the response content
                        image_content = ContentFile(response.content)
                        # Save the image to the offline_pictures directory
                        patient.offline_picture.save(
                            f"offline_{patient.pk}.jpg", image_content
                        )
                        patient.save()
                        print(f"Patient image {patient.name} downloaded")
                        patient.is_image_edited = False
                        patient.save()
            self.stdout.write("Images Downloaded successfully")
        except IntegrityError as e:
            self.stdout.write(f"Something went wrong! Error: {e}")
