from rest_framework import serializers
from clinicmodels.models import Visit
from .patient_serializer import PatientSerializer


class VisitSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Visit
        fields = "__all__"
