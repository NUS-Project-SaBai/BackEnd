from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class OrderSerializer(serializers.ModelSerializer):
    consult = serializers.PrimaryKeyRelatedField(queryset=models.Consult.objects.all())
    visit = serializers.SerializerMethodField()
    medication_review = serializers.PrimaryKeyRelatedField(
        queryset=models.MedicationReview.objects.all(), required=False
    )

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_visit(self, obj):
        return APISerializer.VisitSerializer(obj.consult.visit).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get("include_consult", False):
            representation["consult"] = APISerializer.ConsultSerializer(
                instance.consult
            ).data
        representation["medication_review"] = APISerializer.MedicationReviewSerializer(
            instance.medication_review
        ).data
        return representation
