from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class DiagnosisSerializer(serializers.ModelSerializer):
    consult = serializers.PrimaryKeyRelatedField(queryset=models.Consult.objects.all())

    class Meta:
        model = models.Diagnosis
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["consult"] = APISerializer.ConsultSerializer(
            instance.consult
        ).data
        return representation
