from rest_framework import serializers
from api.serializers.patient_serializer import PatientSerializer
from api.serializers import FileSerializer


class UploadSerializer(serializers.Serializer):
    patient = PatientSerializer()
    files = FileSerializer(many=True)
