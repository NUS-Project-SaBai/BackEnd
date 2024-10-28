from rest_framework import serializers
from api import models
from sabaibiometrics.settings import OFFLINE, CLOUDINARY_URL, BACKEND_API


class PatientSerializer(serializers.ModelSerializer):
    patient_enriched = serializers.SerializerMethodField()
    patient_id = serializers.SerializerMethodField()
    confidence = serializers.SerializerMethodField()

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
    
    def get_confidence(self, patient):
        confidence_dict= self.context.get('confidence', {})
        if not confidence_dict:
            print('List of confidence is empty')
            return ''
        confidence_level = confidence_dict.get(patient.face_encodings, '')
        return confidence_level

    def to_representation(self, instance):
        data = super().to_representation(instance)
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
            "picture": f'{BACKEND_API}/{data["offline_picture"]}' if OFFLINE else f'{CLOUDINARY_URL}/{data["picture"]}',
            "filter_string": self.get_patient_enriched(instance),
            "patient_id": self.get_patient_id(instance),
            "picture": data["picture"],
            "confidence": self.get_confidence(instance),
        }
        return output
