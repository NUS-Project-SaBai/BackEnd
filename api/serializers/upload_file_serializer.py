from rest_framework import serializers
from api import models


class UploadFileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(
        source="patient", queryset=models.Patient.objects.all(), write_only=True
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
