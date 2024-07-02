from rest_framework import serializers
from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ["auth0_id", "username", "email"]


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
            "filter_string": self.get_patient_enriched(instance),
            "patient_id": self.get_patient_id(instance),
        }
        return output


class VisitSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=models.Patient.objects.all())

    class Meta:
        model = models.Visit
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["patient"] = PatientSerializer(instance.patient).data
        return representation


class VitalsSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(
        queryset=models.Visit.objects.all())

    class Meta:
        model = models.Vitals
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["visit"] = VisitSerializer(instance.visit).data
        return representation


class OrderSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=models.Medication.objects.all()
    )
    consult = serializers.PrimaryKeyRelatedField(
        queryset=models.Consult.objects.all())
    visit = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_visit(self, obj):
        return VisitSerializer(obj.consult.visit).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["medicine"] = MedicationSerializer(
            instance.medicine).data
        representation["consult"] = instance.consult.id
        return representation


class ConsultSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(
        queryset=models.Visit.objects.all())
    doctor = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )
    prescriptions = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = models.Consult
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["visit"] = VisitSerializer(instance.visit).data
        representation["doctor"] = UserSerializer(instance.doctor).data
        return representation


class DiagnosisSerializer(serializers.ModelSerializer):
    consult = serializers.PrimaryKeyRelatedField(
        queryset=models.Consult.objects.all())

    class Meta:
        model = models.Diagnosis
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["consult"] = ConsultSerializer(instance.consult).data
        return representation


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Medication
        fields = "__all__"
