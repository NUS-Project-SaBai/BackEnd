from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    auth0_id = models.CharField(max_length=255)
