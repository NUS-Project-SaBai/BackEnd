from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.patient_vision_service import get_patient_vision_viewmodel
from api.serializers.patient_vision_serializer import (
    PatientVisionOutputSerializer,
)


class PatientVisionView(APIView):
    def get(self, request):
        visit_id_raw = request.query_params.get("visit_id")
        try:
            visit_id = int(visit_id_raw)
            if visit_id <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"error": "Missing or invalid visit_id provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        patientVisionViewmodel = get_patient_vision_viewmodel(visit_id)
        patientVisionSerialized = PatientVisionOutputSerializer(patientVisionViewmodel)
        return Response(patientVisionSerialized.data, status=status.HTTP_200_OK)
