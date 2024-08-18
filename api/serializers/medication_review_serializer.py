from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class MedicationReviewSerializer(serializers.ModelSerializer):
    approval = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )
    medicine = serializers.PrimaryKeyRelatedField(
        queryset=models.Medication.objects.all()
    )

    class Meta:
        model = models.MedicationReview
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["approval"] = APISerializer.UserSerializer(
            instance.approval).data
        representation["medicine"] = APISerializer.MedicationSerializer(
            instance.medicine).data
        if self.context.get("include_order", False):
            representation["order"] = APISerializer.OrderSerializer(
                instance.order.first()).data
        return representation
