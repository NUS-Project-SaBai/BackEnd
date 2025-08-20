from rest_framework import serializers


class MedicationHistorySerializer(serializers.Serializer):
    approval_name = serializers.CharField()
    doctor_name = serializers.CharField()
    patient_name = serializers.CharField()
    qty_changed = serializers.IntegerField()
    qty_remaining = serializers.IntegerField()
    date = serializers.DateTimeField()
