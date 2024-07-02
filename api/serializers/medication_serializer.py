from rest_framework import serializers
from api import models


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medication
        fields = "__all__"
