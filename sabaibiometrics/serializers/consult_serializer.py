from rest_framework import serializers
from clinicmodels.models import Consult
from .visit_serializer import VisitSerializer
from .user_serializer import UserSerializer


class ConsultSerializer(serializers.ModelSerializer):
    visit = VisitSerializer()
    doctor = UserSerializer()

    class Meta:
        model = Consult
        fields = "__all__"
