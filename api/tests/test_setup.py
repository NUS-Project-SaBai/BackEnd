import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import CustomUser


class TestSetup(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="test_user",
            email=f"{str(uuid.uuid4())}@email.com",
            auth0_id=1,
        )
        self.client.force_authenticate(user=self.user)
        return super().setUp()

    def tearDown(self):
        self.user.delete()
        return super().tearDown()
