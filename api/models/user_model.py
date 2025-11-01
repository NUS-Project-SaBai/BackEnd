from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    auth0_id = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    ROLE_CHOICES = [("admin", "Admin"), ("member", "Member")]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    is_locked = models.BooleanField(default=False)
