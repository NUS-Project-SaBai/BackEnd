from typing import List
from api.models import Order, Diagnosis
from api.viewmodels.pharmacy_orders_viewmodel import (
    PharmacyOrderVM,
    DiagnosisVM,
    VisitBundleVM,
    PatientHeaderVM,
    PharmacyPatientBundleVM,
)

from collections import defaultdict
from typing import List


def get_pharmacy_orders_viewmodel() -> List[PharmacyPatientBundleVM]:
    # 1) Fetch all pending orders with related consult → visit → patient in ONE query
    filtered_orders = Order.objects.filter(
        medication_review__order_status="PENDING"
    ).select_related("consult", "consult__visit", "consult__visit__patient")

    # 2) We'll group orders by patient → visit
    patient_data_dict = {}
    visit_ids = set()

    # 3) First pass: group orders and remember which visits we saw
    for order in filtered_orders:
        consult = order.consult
        visit = consult.visit
        patient = visit.patient

        if patient not in patient_data_dict:
            patient_data_dict[patient] = {}

        if visit not in patient_data_dict[patient]:
            patient_data_dict[patient][visit] = VisitBundleVM(visit, [], [])
            visit_ids.add(visit.pk)

        patient_data_dict[patient][visit].orders.append(PharmacyOrderVM(order))

    # 4) Batch fetch ALL diagnoses for the visits we saw

    # This dictionary maps visit_ids to a list of all diagnoses made in that visit
    diagnoses_by_visit = defaultdict(list)
    if visit_ids:
        all_diagnoses = Diagnosis.objects.filter(consult__visit_id__in=visit_ids).only(
            "category", "details", "consult__visit_id"
        )
        for diagnosis in all_diagnoses:
            diagnoses_by_visit[diagnosis.consult.visit_id].append(
                DiagnosisVM(diagnosis)
            )

    # 5) Attach diagnoses back into the VisitBundleVMs
    for patient, visits in patient_data_dict.items():
        for visit, visit_viewmodel in visits.items():
            visit_viewmodel.diagnoses = diagnoses_by_visit.get(visit.pk, [])

    # 6) Build final patient bundles
    final_viewmodel_list = []
    for patient, visits in patient_data_dict.items():
        final_viewmodel_list.append(
            PharmacyPatientBundleVM(PatientHeaderVM(patient), list(visits.values()))
        )

    return final_viewmodel_list
