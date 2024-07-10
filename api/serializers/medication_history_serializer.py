from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class MedicationHistorySerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=models.Patient.objects.all(),
        allow_null=True,
        required=False
    )
    doctor = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=models.Medication.objects.all()
    )

    class Meta:
        model = models.MedicationHistory
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.patient:
            representation["patient"] = APISerializer.PatientSerializer(
                instance.patient).data
        representation["doctor"] = APISerializer.UserSerializer(
            instance.doctor).data
        representation["medicine"] = APISerializer.MedicationSerializer(
            instance.medicine).data
        return representation
