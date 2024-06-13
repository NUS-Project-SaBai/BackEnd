from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Medication
from api.serializers import MedicationSerializer


class MedicationView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        medications = Medication.objects.all()
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        medication = Medication.objects.get(pk=pk)
        serializer = MedicationSerializer(medication)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        medication = Medication.objects.get(pk=pk)
        quantityChange = request.data.get("quantityChange", 0)
        data = {"quantity": medication.quantity + quantityChange}
        serializer = MedicationSerializer(medication, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        medication = Medication.objects.get(pk=pk)
        medication.delete()
        return Response({"message": "Deleted successfully"})
