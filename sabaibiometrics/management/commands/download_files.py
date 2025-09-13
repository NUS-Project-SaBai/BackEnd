from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import File
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
from api.utils import file_utils


class Command(BaseCommand):
    help = "Get image from cloudinary to offline"

    def handle(self, *args, **kwargs):
        try:
            files = File.objects.all()
            for file in files:
                if file.file_path:
                    file_url = file_utils.download_file(file.file_path, file.file_name)
                    if file_url:
                        file.offline_file = file_url
                        file.save()
            self.stdout.write("Images Downloaded successfully")
        except IntegrityError as e:
            self.stdout.write(f"Something went wrong! Error: {e}")
