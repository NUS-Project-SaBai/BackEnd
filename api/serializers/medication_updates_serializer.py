from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class MedicationUpdatesSerializer(serializers.ModelSerializer):
    approval = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=models.Medication.objects.all()
    )

    class Meta:
        model = models.MedicationUpdates
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["approval"] = APISerializer.UserSerializer(
            instance.approval).data
        representation["medicine"] = APISerializer.MedicationSerializer(
            instance.medicine).data
        return representation
