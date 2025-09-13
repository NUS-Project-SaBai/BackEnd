from rest_framework import serializers
from api import models


class OrderSerializer(serializers.ModelSerializer):
    consult_id = serializers.PrimaryKeyRelatedField(
        source="consult", queryset=models.Consult.objects.all()
    )
    visit = serializers.SerializerMethodField()

    class Meta:
        model = models.Order
        fields = "__all__"

    def get_visit(self, obj):
        from .visit_serializer import VisitSerializer  # ✅ local import

        return VisitSerializer(obj.consult.visit).data

    def to_representation(self, instance):
        from .medication_review_serializer import (
            MedicationReviewSerializer,
        )  # ✅ local import

        rep = super().to_representation(instance)
        rep["medication_review"] = MedicationReviewSerializer(
            instance.medication_review
        ).data
        return rep
