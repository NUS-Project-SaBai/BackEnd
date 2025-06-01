from django.db import models
from api.models import Patient
from api.models import Visit

class Glasses(models.Model):
    class Meta:
        db_table = "glasses"

    id = models.IntegerField(default=0, primary_key=True)
    left_glasses_degree = models.TextField(blank=True, null=True)
    right_glasses_degree = models.TextField(blank=True, null=True)
    visit_id = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True)