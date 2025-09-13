from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class VitalsSerializer(serializers.ModelSerializer):
    visit_id = serializers.PrimaryKeyRelatedField(
        source="visit",
        queryset=models.Visit.objects.all(),
    )

    class Meta:
        model = models.Vitals
        exclude = ("visit",)
