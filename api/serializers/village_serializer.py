from rest_framework import serializers
from api import models


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Village
        fields = "__all__"
