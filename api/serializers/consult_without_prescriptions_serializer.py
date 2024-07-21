from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class ConsultWithoutPrescriptionsSerializer(serializers.ModelSerializer):
    visit = serializers.PrimaryKeyRelatedField(
        queryset=models.Visit.objects.all())
    doctor = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )

    class Meta:
        model = models.Consult
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["visit"] = APISerializer.VisitSerializer(
            instance.visit).data
        representation["doctor"] = APISerializer.UserSerializer(
            instance.doctor).data
        return representation
