from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from api.models import Medication, MedicationReview
from api.serializers import MedicationSerializer
from api.services.medication_review_service import create_medication_review


def list_medications():
    return Medication.objects.all().order_by("medicine_name")


def get_medication(pk):
    return get_object_or_404(Medication, pk=pk)


def get_medication_with_pending(pk, order_status):
    medication = Medication.objects.get(pk=pk)
    pending_sum = (
        MedicationReview.objects.filter(
            medicine_id=pk, order_status=order_status
        ).aggregate(Sum("quantity_changed"))["quantity_changed__sum"]
        or 0
    )

    return {
        "medicine_id": pk,
        "medicine_name": medication.medicine_name,
        "notes": medication.notes,
        "pending_quantity": pending_sum,
        "current_quantity": medication.quantity,
        "code": medication.code,
    }


@transaction.atomic
def create_medication(data, doctor_id):
    serializer = MedicationSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    medication = serializer.save()

    review_data = {
        "approval": doctor_id,
        "quantity_changed": medication.quantity,
        "quantity_remaining": medication.quantity,
        "medicine": medication.pk,
        "order_status": "APPROVED",
    }
    create_medication_review(review_data)
    return medication


@transaction.atomic
def update_medication(pk, update_data, doctor_id):
    medication = Medication.objects.get(pk=pk)
    quantity_change = update_data.get("quantityChange", 0)
    new_quantity = medication.quantity + quantity_change

    data = {
        "medicine_name": update_data.get("medicine_name", medication.medicine_name),
        "quantity": new_quantity,
        "notes": update_data.get("notes", medication.notes),
        "code": update_data.get("code", medication.code),
        "warning_quantity": update_data.get(
            "warning_quantity", medication.warning_quantity
        ),
    }

    serializer = MedicationSerializer(medication, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    review_data = {
        "approval": doctor_id,
        "quantity_changed": quantity_change,
        "quantity_remaining": new_quantity,
        "medicine": medication.pk,
        "order_status": "APPROVED",
    }
    create_medication_review(review_data)
    return serializer.data


def update_quantity(pk, quantity_change):
    medication = Medication.objects.get(pk=pk)
    serializer = MedicationSerializer(
        medication,
        data={"quantity": medication.quantity + quantity_change},
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
