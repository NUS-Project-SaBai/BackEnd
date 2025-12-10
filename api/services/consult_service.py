from django.db import transaction
from rest_framework.exceptions import NotFound

from api.models import Consult, Diagnosis
from api.serializers import ConsultSerializer, DiagnosisSerializer
from api.services.diagnosis_service import create_diagnosis  # to be created
from api.services.orders_service import create_order  # to be created
from api.utils import doctor_utils


def list_consults_by_visit_id(visit_id=None):
    qs = Consult.objects.all()
    if visit_id:
        qs = qs.filter(visit=visit_id)
    return qs


def list_consults_by_patient_id(patient_id=None):
    qs = Consult.objects.all()
    if patient_id:
        qs = qs.filter(visit__patient__pk=patient_id)
    return qs


def get_consult(pk):
    return Consult.objects.filter(pk=pk).first()


@transaction.atomic
def create_consult(data, user_headers):
    consult_data = data.copy()
    del consult_data["diagnoses"]
    del consult_data["orders"]
    consult_data["doctor_id"] = doctor_utils.get_doctor_id(user_headers)
    serializer = ConsultSerializer(data=consult_data)
    serializer.is_valid(raise_exception=True)
    consult = serializer.save()

    for order_data in data.get("orders", []):
        order_data["consult_id"] = consult.pk
        create_order(order_data)

    for diagnosis_data in data.get("diagnoses", []):
        diagnosis_data["consult_id"] = consult.pk
        create_diagnosis(diagnosis_data)

    return serializer


@transaction.atomic
def update_consult_service(pk, data):
    """
    Updates a consult and manages the lifecycle (Creation, Update, Deletion)
    """
    try:
        # Prevent race conditions by locking the consult
        consult = Consult.objects.select_for_update().get(pk=pk)
    except Consult.DoesNotExist:
        raise NotFound(f"Consult with id {pk} not found")

    consult_fields = {k: v for k, v in data.items() if k not in ["diagnoses"]}

    serializer = ConsultSerializer(consult, data=consult_fields, partial=True)
    if serializer.is_valid(raise_exception=True):
        consult = serializer.save()

    incoming_diagnoses = data.get("diagnoses", [])
    _upsert_diagnoses(consult, incoming_diagnoses)

    # Return refreshed data
    return ConsultSerializer(consult).data


def _upsert_diagnoses(consult, incoming_data):
    """
    Compares existing diagnoses with incoming list to determine
    creation of new diagnoses, updates of existing diagnoses, and deletion of removed diagnoses.
    """
    existing_map = {d.id: d for d in Diagnosis.objects.filter(consult=consult)}
    existing_ids = set(existing_map.keys())

    incoming_map = {item.get("id"): item for item in incoming_data if item.get("id")}
    incoming_ids = set(incoming_map.keys())

    # Delete (Existing in original except for the ones in incoming)
    to_delete_ids = existing_ids - incoming_ids
    if to_delete_ids:
        Diagnosis.objects.filter(id__in=to_delete_ids).delete()

    # Update (Present in both)
    to_update_ids = existing_ids & incoming_ids
    for diag_id in to_update_ids:
        current_diagnosis = existing_map[diag_id]
        new_data = incoming_map[diag_id]

        serializer = DiagnosisSerializer(current_diagnosis, data=new_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # Create (No ID provided )
    for item in incoming_data:
        if not item.get("id"):
            Diagnosis.objects.create(
                consult=consult,
                category=item.get("category"),
                details=item.get("details"),
            )
