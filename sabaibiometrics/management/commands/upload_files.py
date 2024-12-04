from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import File
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
from api.views import utils


class Command(BaseCommand):
    help = "Upload local files to google drive"

    def handle(self, *args, **kwargs):
        try:
            files = File.objects.all()
            for file in files:
                if file.offline_file:
                    file_url = utils.upload_file(file.offline_file.path, file.file_name)
                    file.file_path = file_url
                    file.save()
            self.stdout.write("Files uploaded successfully")
        except IntegrityError as e:
            self.stdout.write(f"Something went wrong! Error: {e}")
