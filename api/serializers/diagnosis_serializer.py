from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class DiagnosisSerializer(serializers.ModelSerializer):
    consult_id = serializers.PrimaryKeyRelatedField(
        source="consult", queryset=models.Consult.objects.all()
    )

    class Meta:
        model = models.Diagnosis
        fields = "__all__"
