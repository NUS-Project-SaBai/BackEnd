from rest_framework import serializers

from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username"]


class PatientSerializer(serializers.ModelSerializer):
    patientEnriched = serializers.SerializerMethodField()

    class Meta:
        model = models.Patient
        fields = "__all__"

    def get_patientEnriched(self, patient):
        # Perform any enrichment logic here
        # For example, concatenating patient name and id
        return (
            f"{patient.village_prefix}"
            + f"{patient.pk}".zfill(3)
            + f"{patient.village_prefix}{patient.pk} {patient.contact_no} {patient.name}"
        )

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
            "drug_allergy": data["drug_allergy"],
            "face_encodings": data["face_encodings"],
            "picture": data["picture"],
            "filterString": self.get_patientEnriched(instance),
        }
        return output


class VisitSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = models.Visit
        fields = "__all__"


class VitalsSerializer(serializers.ModelSerializer):
    visit = VisitSerializer()

    class Meta:
        model = models.Vitals
        fields = "__all__"


class ConsultSerializer(serializers.ModelSerializer):
    visit = VisitSerializer()
    doctor = UserSerializer()

    class Meta:
        model = models.Consult
        fields = "__all__"


class DiagnosisSerializer(serializers.ModelSerializer):
    consult = serializers.PrimaryKeyRelatedField(queryset=models.Consult.objects.all())

    class Meta:
        model = models.Diagnosis
        fields = "__all__"


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medication
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    medicine = MedicationSerializer()
    consult = ConsultSerializer()

    class Meta:
        model = models.Order
        fields = "__all__"
