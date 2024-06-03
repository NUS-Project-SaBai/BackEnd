from rest_framework import serializers
from clinicmodels.models import Diagnosis
from .consult_serializer import ConsultSerializer

class DiagnosisSerializer(serializers.ModelSerializer):
    consult = ConsultSerializer()

    class Meta:
        model = Diagnosis
        fields = "__all__"
