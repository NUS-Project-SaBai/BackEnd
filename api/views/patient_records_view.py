from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.patient_records_service import get_patient_record_viewmodel
from api.serializers.patient_records_serializer import PatientRecordsOutputSerializer


class PatientRecordsView(APIView):
    def get(self, request):
        visit_id = request.query_params.get("visit")
        if not visit_id:
            return Response({"error": "Missing visit param"}, status=400)

        patientRecordsViewModel = get_patient_record_viewmodel(visit_id)
        patientRecordsSerialized = PatientRecordsOutputSerializer(
            patientRecordsViewModel
        )
        return Response(patientRecordsSerialized.data)
