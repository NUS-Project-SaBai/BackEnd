from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.patient_records_service import get_patient_record_viewmodel
from api.serializers.patient_records_serializer import PatientRecordsOutputSerializer


class PatientRecordsView(APIView):
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

        patientRecordsViewModel = get_patient_record_viewmodel(visit_id)
        patientRecordsSerialized = PatientRecordsOutputSerializer(
            patientRecordsViewModel
        )
        return Response(patientRecordsSerialized.data)
