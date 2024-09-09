from rest_framework import serializers
from clinicmodels.models import Vitals
from .visit_serializer import VisitSerializer


class VitalsSerializer(serializers.ModelSerializer):
    visit = VisitSerializer()

    class Meta:
        model = Vitals
        fields = "__all__"
