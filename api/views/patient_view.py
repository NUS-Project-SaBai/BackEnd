import json
from requests import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from sabaibiometrics.settings import OFFLINE
from api.types.vitals_types import VitalsRegistrationAPIData
from api.types.patient_types import PatientAPIData, RegstriationAPIData
from api.models import Patient
from api.serializers import PatientSerializer
from api.services.patient_service import (
    extract_and_clean_picture,
    generate_face_encoding,
    create_patient_with_vitals,
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

    def post(self, request: Request) -> Response:
        # Parse Request Payload
        payload: RegstriationAPIData = request.data
        pictureData: bytes = payload["picture"]
        patientData: PatientAPIData = json.loads(payload["patient"])
        vitalsData: VitalsRegistrationAPIData = json.loads(payload["vitals"])

        patientDataWithPicture: PatientAPIData = extract_and_clean_picture(
            patientData, pictureData
        )
        face_encoding: str = generate_face_encoding(patientDataWithPicture)

        serializer: PatientSerializer = create_patient_with_vitals(
            patientData=patientDataWithPicture,
            face_encoding=face_encoding,
            vitalsData=vitalsData,
        )
        return Response(serializer.data)

    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        data = request.data.copy()
        if OFFLINE:
            picture = data.get("picture", None)
            if picture:
                data["offline_picture"] = picture
            data.pop("picture", None)
        face_encoding = generate_face_encoding(data)

        serializer = PatientSerializer(patient, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(face_encodings=face_encoding)
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})
