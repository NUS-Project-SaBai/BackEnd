from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.models import Patient
from api.serializers import PatientSerializer
from api.services.patient_service import (
    extract_and_clean_picture,
    generate_face_encoding,
    create_patient_with_temperature
)
from api.services.visit_service import (
    annotate_with_last_visit,
    get_patient_with_last_visit_by_patient_pk,
)


class PatientView(APIView):
    def get(self, request, pk=None):
        if pk:
            patient = get_patient_with_last_visit_by_patient_pk(patientPk=pk)
            return Response(PatientSerializer(patient).data)

        patients = annotate_with_last_visit(Patient.objects).order_by(
            "-last_visit_date", "-pk"
        )

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

        serializer = create_patient_with_temperature(data=data, face_encoding=face_encoding)
        return Response(serializer.data)

    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        data = extract_and_clean_picture(request.data.copy())
        face_encoding = generate_face_encoding(data)

        serializer = PatientSerializer(patient, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(face_encodings=face_encoding)
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})
