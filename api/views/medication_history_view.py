# In medication_history.py

from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.medication_history_service import get_medication_history_viewmodel
from api.serializers.medication_history_serializer import MedicationHistorySerializer

class MedicationHistoryView(APIView):
    def get(self, request):
        medicine_id = request.query_params.get("medicine_id")
        medication_history = get_medication_history_viewmodel(medicine_id)
        medication_history_serialized = MedicationHistorySerializer(medication_history, many=True)
        return Response(medication_history_serialized.data)