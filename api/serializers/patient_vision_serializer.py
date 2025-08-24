from rest_framework import serializers
from api.serializers import PatientSerializer, GlassesSerializer

class VitalsVisionPickOut(serializers.Serializer):
    right_eye_degree  = serializers.CharField(allow_null=True, required=False)
    left_eye_degree   = serializers.CharField(allow_null=True, required=False)
    right_eye_pinhole = serializers.CharField(allow_null=True, required=False)
    left_eye_pinhole  = serializers.CharField(allow_null=True, required=False)

class PatientVisionVMOut(serializers.Serializer):
    patient = PatientSerializer()
    vision  = GlassesSerializer(allow_null=True)
    vitals   = VitalsVisionPickOut(allow_null=True)
