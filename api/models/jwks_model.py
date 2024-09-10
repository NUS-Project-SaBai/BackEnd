from django.db import models
from django.db.models import JSONField  # If using PostgreSQL


class JWKS(models.Model):
    jwks = JSONField()  # Use models.TextField() if JSONField is not available
    updated_at = models.DateTimeField(auto_now=True)