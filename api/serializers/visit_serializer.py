from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class VisitSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=models.Patient.objects.all())

    class Meta:
        model = models.Visit
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["patient"] = APISerializer.PatientSerializer(
            instance.patient
        ).data
        return representation
