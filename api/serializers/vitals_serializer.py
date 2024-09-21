from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class VitalsSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(
        queryset=models.Visit.objects.all())

    class Meta:
        model = models.Vitals
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["visit"] = APISerializer.VisitSerializer(
            instance.visit).data
        return representation
