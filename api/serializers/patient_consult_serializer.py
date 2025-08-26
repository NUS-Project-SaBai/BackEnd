from rest_framework import serializers
from api.serializers import PatientSerializer
from api.serializers import VitalsSerializer


class DoctorMiniOut(serializers.Serializer):
    nickname = serializers.CharField(allow_null=True, required=False)


class ConsultPickOut(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    doctor = DoctorMiniOut()
    referred_for = serializers.CharField(allow_null=True, required=False)


class PrescriptionRowOut(serializers.Serializer):
    consult_id = serializers.IntegerField(allow_null=True)
    visit_date = serializers.CharField(allow_null=True)
    medication = serializers.CharField(allow_null=True)
    quantity = serializers.IntegerField(allow_null=True)
    notes = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField(allow_null=True)


class PatientConsultOutputSerializer(serializers.Serializer):
    patient = PatientSerializer()
    vitals = VitalsSerializer(allow_null=True)
    visit_date = serializers.CharField()
    consults = ConsultPickOut(many=True)
    prescriptions = PrescriptionRowOut(many=True)
