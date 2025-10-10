from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class FileSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        source="patient", queryset=models.Patient.objects.all(), write_only=True
    )
    patient = APISerializer.PatientSerializer(read_only=True)

    class Meta:
        model = models.File
        fields = "__all__"
