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
    
        diagnosis_list = []
        if patient not in patient_data_dict:
            patient_data_dict[patient] = {}
        
        if visit not in patient_data_dict[patient]:
            visit_diagnosis = Diagnosis.objects.filter(consult=consult).only("category", "details")
            for diagnosis in visit_diagnosis:
                diagnosis_list.append(DiagnosisVM(diagnosis))
            
            patient_data_dict[patient][visit] = VisitBundleVM(visit, [], diagnosis_list)
    
        patient_data_dict[patient][visit].orders.append(PharmacyOrderVM(order))

    final_viewmodel_list = []
    for patient, visit in patient_data_dict.items():
        final_viewmodel_list.append(PharmacyPatientBundleVM(PatientHeaderVM(patient), list(patient_data_dict[patient].values())))
    return final_viewmodel_list