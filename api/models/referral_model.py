from django.db import models
from django.utils import timezone
from api.models import Consult

class Referrals(models.Model):
    class Meta:
        db_table = "referrals"

    referral_state = models.TextField(blank=True, null=True)
    referral_comments = models.TextField(blank=True, null=True)
    consult = models.ForeignKey(Consult, on_delete=models.SET_NULL, blank=True, null=True)


