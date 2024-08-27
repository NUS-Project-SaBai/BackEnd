from rest_framework import serializers
from api import models


class PatientSerializer(serializers.ModelSerializer):
    patient_enriched = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Patient
        fields = "__all__"

    def get_patient_enriched(self, patient):
        return (
            f"{patient.village_prefix}"
            + f"{patient.pk}".zfill(3)
            + f"{patient.village_prefix}{patient.pk} {patient.contact_no} {patient.name}"
        )

    def get_patient_id(self, patient):
        return f"{patient.village_prefix}" + f"{patient.pk}".zfill(3)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        output = {
            "model": "clinicmodels.patient",
            "pk": data["id"],
            "village_prefix": data["village_prefix"],
            "name": data["name"],
            "identification_number": data["identification_number"],
            "contact_no": data["contact_no"],
            "gender": data["gender"],
            "date_of_birth": data["date_of_birth"],
            "poor": data["poor"],
            "bs2": data["bs2"],
            "drug_allergy": data["drug_allergy"],
            "face_encodings": data["face_encodings"],
            "picture": data["picture"],
            "offline_picture": data["offline_picture"],
            "filter_string": self.get_patient_enriched(instance),
            "patient_id": self.get_patient_id(instance),
        }
        return output
