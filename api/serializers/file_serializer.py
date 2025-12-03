from rest_framework import serializers
from api import models


class FileSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        source="patient", queryset=models.Patient.objects.all()
    )

    class Meta:
        model = models.File
        fields = [
            "id",
            "patient_id",
            "file_path",
            "offline_file",
            "file_name",
            "description",
            "created_at",
            "is_deleted",
        ]
