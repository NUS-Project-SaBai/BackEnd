from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Create default users"

    def handle(self, *args, **kwargs):
        subprocess.run("python manage.py makemigrations", shell=True, text=True)
        subprocess.run("python manage.py migrate", shell=True, text=True)
        subprocess.run("python manage.py set_auth0_users", shell=True, text=True)
        subprocess.run("python manage.py runserver 0.0.0.0:8000", shell=True, text=True)
