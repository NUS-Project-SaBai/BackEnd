from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import subprocess


class Command(BaseCommand):
    help = "Create default users"

    def handle(self, *args, **kwargs):
        subprocess.run(["python", "manage.py", "makemigrations"])
        subprocess.run(["python", "manage.py", "migrate"])
        subprocess.run(["python", "manage.py", "set_auth0_users"])
        subprocess.run(["python", "manage.py", "runserver"])
