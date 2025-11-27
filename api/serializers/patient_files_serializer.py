from rest_framework import serializers
from api.serializers.patient_serializer import PatientSerializer
from api.serializers import FileSerializer


class PatientFilesSerializer(serializers.Serializer):
    """Serializer for grouping a patient with their associated files."""
    patient = PatientSerializer()
    files = FileSerializer(many=True)
