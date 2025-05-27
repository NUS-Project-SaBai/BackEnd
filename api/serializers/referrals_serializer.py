from rest_framework import serializers
from api import models
from api import serializers as APISerializer

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Referrals
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation