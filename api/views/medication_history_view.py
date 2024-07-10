from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import MedicationHistory
from api.serializers import MedicationHistorySerializer


class MedicationHistoryView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        medication_history = MedicationHistory.objects.all()
        medication_pk = request.query_params.get("medication_pk", "")
        if medication_pk:
            medication_history = medication_history.filter(
                medicine_id=medication_pk)
        serializer = MedicationHistorySerializer(medication_history, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        medication_history = MedicationHistory.objects.filter(pk=pk).first()
        serializer = MedicationHistorySerializer(medication_history)
        return Response(serializer.data)

    def post(self, request):
        MedicationHistoryView.new_entry(request.data)

    def patch(self, request, pk):
        medication_history = MedicationHistory.objects.get(pk=pk)
        serializer = MedicationHistorySerializer(
            medication_history, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        medication_history = MedicationHistory.objects.get(pk=pk)
        medication_history.delete()
        return Response({"message": "Deleted successfully"})

    @staticmethod
    def new_entry(data):
        serializer = MedicationHistorySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
