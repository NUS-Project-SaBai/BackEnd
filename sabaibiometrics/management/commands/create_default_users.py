from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Create default users"

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_user(username="test_user1", password="test_user1")
            User.objects.create_user(username="test_user2", password="test_user2")
            User.objects.create_user(username="test_doc1", password="test_doc1")
            self.stdout.write("Default users created successfully")
        except IntegrityError:
            self.stdout.write("Default users already exist")
