from rest_framework.response import Response
from api.models import Medication
from api.serializers import MedicationSerializer
from sabaibiometrics.utils import get_doctor_id
from api.views import MedicationHistoryView
from django.db import transaction


def update_medication(data, pk):
    medication = Medication.objects.get(pk=pk)
    quantityChange = data.get("quantityChange", 0)
    data = {
        "medicine_name": data.get(
            "medicine_name", medication.medicine_name
        ),
        "quantity": medication.quantity + quantityChange,
        "notes": data.get("notes", medication.notes),
    }
    serializer = MedicationSerializer(medication, data=data, partial=True)
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
