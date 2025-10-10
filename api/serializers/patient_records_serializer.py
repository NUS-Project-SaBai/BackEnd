from rest_framework import serializers
from api.serializers import PatientSerializer, VitalsSerializer


class DoctorMiniSerializer(serializers.Serializer):
    nickname = serializers.CharField()


class ConsultMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    doctor = DoctorMiniSerializer()
    referred_for = serializers.CharField()


class PrescriptionMiniSerializer(serializers.Serializer):
    consult_id = serializers.IntegerField()
    visit_date = serializers.DateTimeField()
    medication = serializers.CharField()
    quantity = serializers.IntegerField()
    notes = serializers.CharField()
    status = serializers.CharField()


class PatientRecordsOutputSerializer(serializers.Serializer):
    patient = PatientSerializer()
    vitals = VitalsSerializer(allow_null=True)
    visit_date = serializers.DateTimeField()
    consults = serializers.ListSerializer(child=ConsultMiniSerializer())
    prescriptions = serializers.ListSerializer(child=PrescriptionMiniSerializer())
