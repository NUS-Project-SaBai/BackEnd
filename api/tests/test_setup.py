import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import User


class TestSetup(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user",
            email=f"{str(uuid.uuid4())}@email.com",
        )
