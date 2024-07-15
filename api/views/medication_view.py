from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Medication
from api.serializers import MedicationSerializer
from api.views.utils import get_doctor_id
from api.views import MedicationHistoryView
from django.db import transaction


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
            with transaction.atomic():
                medication = serializer.save()
                doctor_id = get_doctor_id(request)
                medication_history_data = {
                    "doctor": doctor_id,
                    "quantity_changed": medication.quantity,
                    "quantity_remaining": medication.quantity,
                    "medicine": medication.pk,
                }
                MedicationHistoryView.new_entry(medication_history_data)
            return Response(serializer.data)

    def patch(self, request, pk):
        print(request, pk)
        medication = Medication.objects.get(pk=pk)
        quantityChange = request.data.get("quantityChange", 0)
        data = {
            "medicine_name": request.data.get(
                "medicine_name", medication.medicine_name
            ),
            "quantity": medication.quantity + quantityChange,
            "notes": request.data.get("notes", medication.notes),
        }
        serializer = MedicationSerializer(medication, data=data, partial=True)

        doctor_id = get_doctor_id(request)
        medication_history_data = {
            "doctor": doctor_id,
            "quantity_changed": quantityChange,
            "quantity_remaining": medication.quantity + quantityChange,
            "medicine": medication.pk,
        }

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                MedicationHistoryView.new_entry(medication_history_data)
                serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        medication = Medication.objects.get(pk=pk)
        medication.delete()
        return Response({"message": "Deleted successfully"})

    def update_quantity(self, quantityChange, pk):
        medication = Medication.objects.get(pk=pk)
        data = {
            "quantity": medication.quantity + quantityChange,
        }
        serializer = MedicationSerializer(medication, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
