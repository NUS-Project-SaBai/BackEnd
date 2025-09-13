from api.models import Consult
from api.serializers import ConsultSerializer
from api.utils import doctor_utils
from django.db import transaction

from api.services.orders_service import create_order  # to be created
from api.services.diagnosis_service import create_diagnosis  # to be created


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
    consult_data = data.get("consult")
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
