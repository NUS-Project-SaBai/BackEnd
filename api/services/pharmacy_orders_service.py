# from api.viewmodels.patient_records_viewmodel import PatientRecordViewModel
# from api.models import Order
# from api.services import visit_service, vitals_service, consult_service

from collections import defaultdict
from typing import List
from api.models import Order, Diagnosis, Visit, Patient
from api.viewmodels.pharmacy_orders_viewmodel import (
    PharmacyOrderVM, DiagnosisVM, VisitBundleVM, PatientHeaderVM, PharmacyPatientBundleVM
)

def get_pharmacy_orders_viewmodel() -> List[PharmacyPatientBundleVM]:
    orders_qs = (
        Order.objects
        .select_related(
            "consult",
            "consult__visit",
            "consult__visit__patient",
            "medication_review",
            "medication_review__medicine",
        )
        .order_by("-consult__visit__date", "pk")
    )

    buckets = defaultdict(lambda: {"patient": None, "visits": {}})

    for o in orders_qs:
        visit = o.consult.visit
        patient = visit.patient
        pkey = patient.pk

        # patient header (set once)
        if buckets[pkey]["patient"] is None:
            buckets[pkey]["patient"] = PatientHeaderVM(
                patient_id=getattr(patient, "patient_id", str(patient.pk)),
                name=getattr(patient, "name", str(patient)),
                picture_url=getattr(getattr(patient, "picture", None), "url", None),
                village_prefix=str(getattr(patient, "village_prefix", "")) or "",
            )

        vb = buckets[pkey]["visits"].get(visit.pk)
        if vb is None:
            vb = {"visit": visit, "orders": []}
            buckets[pkey]["visits"][visit.pk] = vb

        mr = getattr(o, "medication_review", None)
        med = getattr(mr, "medicine", None) if mr else None
        vb["orders"].append(
            PharmacyOrderVM(
                id=o.pk,
                medication_name=getattr(med, "medicine_name", None),
                medication_code=getattr(med, "medicine_code", None),
                quantity_changed=getattr(mr, "quantity_changed", None) if mr else None,
                notes=getattr(o, "notes", None),
            )
        )

    out: List[PharmacyPatientBundleVM] = []

    for bundle in buckets.values():
        header: PatientHeaderVM = bundle["patient"]

        visit_entries = sorted(
            bundle["visits"].values(),
            key=lambda v: getattr(v["visit"], "date", None),
            reverse=True,
        )

        visit_vms: List[VisitBundleVM] = []
        for ve in visit_entries:
            visit = ve["visit"]

            diag_rows = Diagnosis.objects.filter(consult__visit=visit).only("category", "details")
            diags = [DiagnosisVM(category=d.category, details=d.details) for d in diag_rows]

            visit_vms.append(
                VisitBundleVM(
                    orders=ve["orders"],
                    diagnoses=diags,
                    visit_id=visit.pk,
                    visit_date=getattr(visit, "date", None),
                )
            )

        out.append(PharmacyPatientBundleVM(patient=header, data=visit_vms))

    return out
