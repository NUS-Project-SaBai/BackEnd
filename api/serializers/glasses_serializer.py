from rest_framework import serializers
from api import models
from api import serializers as APISerializer

class GlassesSerializer(serializers.ModelSerializer):
    visit_id = serializers.IntegerField(source="visit.id", read_only=True)

    class Meta:
        model = models.Glasses
        fields = [
            "id",
            "left_glasses_degree",
            "right_glasses_degree",
            "visit_id",
        ]
