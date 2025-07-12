from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class VitalsSerializer(serializers.ModelSerializer):
    visit_id = serializers.PrimaryKeyRelatedField(
        source="visit", queryset=models.Visit.objects.all(), write_only=True
    )
    visit = APISerializer.VisitSerializer(read_only=True)

    class Meta:
        model = models.Vitals
        fields = "__all__"
