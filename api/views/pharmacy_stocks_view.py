# In pharmacy_stocks_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.pharmacy_stocks_service import get_medication_history_viewmodel
from api.serializers.pharmacy_stocks_serializer import MedicationHistorySerializer

class MedicationHistoryView(APIView):
    def get(self, request, medicine_id):
        # Fetch the medication history for a specific medicine
        medication_history = get_medication_history_viewmodel(medicine_id)
        medication_history_serialized = MedicationHistorySerializer(medication_history, many=True)
        return Response(medication_history_serialized.data)

