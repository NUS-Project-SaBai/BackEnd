from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class OrderSerializer(serializers.ModelSerializer):
    consult = serializers.PrimaryKeyRelatedField(
        queryset=models.Consult.objects.all())
    visit = serializers.SerializerMethodField()
    medication_updates = serializers.PrimaryKeyRelatedField(
        queryset=models.MedicationUpdates.objects.all(), required=False
    )

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_visit(self, obj):
        return APISerializer.VisitSerializer(obj.consult.visit).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["medication_updates"] = APISerializer.MedicationUpdatesSerializer(
            instance.medication_updates
        ).data
        representation["consult"] = APISerializer.ConsultWithoutPrescriptionsSerializer(
            instance.consult).data
        return representation
