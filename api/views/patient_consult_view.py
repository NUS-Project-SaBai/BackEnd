from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.patient_consult_services import get_patient_consult_viewmodel
from api.serializers.patient_consult_serializer import PatientConsultOutputSerializer


class PatientConsultView(APIView):
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

        patientConsultViewmodel = get_patient_consult_viewmodel(visit_id)
        patientConsultSerialized = PatientConsultOutputSerializer(
            patientConsultViewmodel
        )
        return Response(patientConsultSerialized.data, status=status.HTTP_200_OK)
