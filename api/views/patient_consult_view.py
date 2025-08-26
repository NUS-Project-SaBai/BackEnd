from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.patient_consult_services import get_patient_consult_viewmodel
from api.serializers.patient_consult_serializer import (
    PatientConsultOutputSerializer,
    ConsultPickOut,
    PrescriptionRowOut,
)
from api.serializers import VitalsSerializer


class PatientConsultView(APIView):
    def get(self, request):
        visit_id_raw = request.query_params.get("visit_id")
        try:
            visit_id = int(visit_id_raw or "0")
        except ValueError:
            return Response(
                {"detail": "visit_id must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if visit_id <= 0:
            return Response(
                {"detail": "visit_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        PatientConsultViewmodel = get_patient_consult_viewmodel(visit_id)
        return Response(
            PatientConsultOutputSerializer(PatientConsultViewmodel).data,
            status=status.HTTP_200_OK,
        )
