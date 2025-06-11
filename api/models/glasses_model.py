from django.db import models
from api.models import Visit

class Glasses(models.Model):
    class Meta:
        db_table = "glasses_prescription"

    left_glasses_degree = models.CharField(max_length=20, blank=True, null=True)
    right_glasses_degree = models.CharField(max_length=20, blank=True, null=True)
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)