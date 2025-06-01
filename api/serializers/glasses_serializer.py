from rest_framework import serializers
from api import models
from api import serializers as APISerializer

class GlassesSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(
        queryset=models.Visit.objects.all())

    class Meta:
        model = models.Glasses
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["patient"] = APISerializer.PatientSerializer(
            instance.visit.patient
        ).data
        return representation
