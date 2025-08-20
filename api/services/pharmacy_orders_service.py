from typing import List
from api.models import Order, Diagnosis
from api.viewmodels.pharmacy_orders_viewmodel import (
    PharmacyOrderVM, DiagnosisVM, VisitBundleVM, PatientHeaderVM, PharmacyPatientBundleVM
)

def get_pharmacy_orders_viewmodel() -> List[PharmacyPatientBundleVM]:
    filtered_orders = (Order.objects
        .filter(medication_review__order_status="PENDING")
    )
    patient_data_dict = {}

    for order in filtered_orders:
        consult = order.consult
        visit = consult.visit if consult else None
        patient = visit.patient if visit else None
    
        pharmacy_orders_list = []
        diagnosis_list = []
        
        pharmacy_orders_list.append(
            PharmacyOrderVM(order)
        )
        visit_diagnosis = Diagnosis.objects.filter(consult=consult).only("category", "details")
        for diagnosis in visit_diagnosis:
            diagnosis_list.append(DiagnosisVM(diagnosis))

        if patient not in patient_data_dict:
            patient_data_dict[patient] = []
        
        patient_data_dict[patient].append(VisitBundleVM(visit, pharmacy_orders_list, diagnosis_list))

    final_viewmodel_list = []
    for patient in patient_data_dict:
        final_viewmodel_list.append(PharmacyPatientBundleVM(PatientHeaderVM(patient), patient_data_dict[patient]))
    return final_viewmodel_list