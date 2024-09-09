from rest_framework import serializers
from clinicmodels.models import Order
from .medication_serializer import MedicationSerializer
from .consult_serializer import ConsultSerializer


class OrderSerializer(serializers.ModelSerializer):
    medicine = MedicationSerializer()
    consult = ConsultSerializer()

    class Meta:
        model = Order
        fields = "__all__"
