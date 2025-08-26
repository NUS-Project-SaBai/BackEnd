from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from api.models import Visit, Patient, Vitals, Consult, Order
from api.viewmodels.patient_consult_viewmodel import PatientConsultViewModel


def _qs_patient() -> QuerySet:
    return Patient.objects


def _qs_consults(visit_id: int) -> QuerySet:
    return (
        Consult.objects.filter(visit_id=visit_id)
        .select_related("doctor")
        .order_by("date", "id")
    )


def _qs_orders_for_visit(visit_id: int) -> QuerySet:
    return (
        Order.objects.filter(consult__visit_id=visit_id)
        .select_related(
            "consult",
            "consult__visit",
            "medication_review",
            "medication_review__medicine",
        )
        .order_by("id")
    )


def get_patient_consult_viewmodel(visit_id: int) -> PatientConsultViewModel:
    visit: Visit = get_object_or_404(
        Visit.objects.select_related("patient").only("id", "patient_id", "date"),
        pk=visit_id,
    )

    patient: Patient = _qs_patient().get(pk=visit.patient_id)

    vitals: Optional[Vitals] = (
        Vitals.objects.filter(visit_id=visit_id).order_by("-id").first()
    )

    consults: List[Consult] = list(_qs_consults(visit_id))
    orders: List[Order] = list(_qs_orders_for_visit(visit_id))

    return PatientConsultViewModel(
        patient=patient,
        vitals=vitals,
        visit=visit,
        consults=consults,
        orders=orders,
    )
