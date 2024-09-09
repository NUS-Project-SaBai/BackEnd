from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class OrderSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=models.Medication.objects.all()
    )
    consult = serializers.PrimaryKeyRelatedField(queryset=models.Consult.objects.all())
    visit = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_visit(self, obj):
        return APISerializer.VisitSerializer(obj.consult.visit).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["medicine"] = APISerializer.MedicationSerializer(
            instance.medicine
        ).data
        representation["consult"] = instance.consult.id
        return representation
