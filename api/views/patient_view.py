from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.models import Patient
from api.serializers import PatientSerializer
from api.services.patient_service import (
    extract_and_clean_picture,
    generate_face_encoding,
)


class PatientView(APIView):

    def get(self, request, pk=None):
        if pk:
            patient = get_object_or_404(Patient, pk=pk)
            return Response(PatientSerializer(patient).data)

        patients = Patient.objects.order_by("-pk")
        name = request.query_params.get("name")
        code = request.query_params.get("village_code")

        if name:
            patients = patients.filter(name__iexact=name)
        if code:
            patients = patients.filter(village_prefix__iexact=code)

        return Response(PatientSerializer(patients, many=True).data)

    def post(self, request):
        data = extract_and_clean_picture(request.data.copy())
        face_encoding = generate_face_encoding(data)

        serializer = PatientSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(face_encodings=face_encoding)
        return Response(serializer.data)

    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        data = extract_and_clean_picture(request.data.copy())

        serializer = PatientSerializer(patient, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})
