from api.viewmodels.patient_records_viewmodel import PatientRecordViewModel
from api.models import Order
from api.services import visit_service, vitals_service, consult_service


def get_patient_record_viewmodel(visit_id) -> PatientRecordViewModel:
    visit = visit_service.get_visit(pk=visit_id)
    if not visit:
        return None

    patient = visit.patient
    vitals = vitals_service.list_vitals(visit_id=visit_id).first()
    consults = consult_service.list_consults(visit_id=visit.pk)
    prescriptions = Order.objects.filter(consult__visit=visit).select_related(
        "medication_review__medicine"
    )

    return PatientRecordViewModel(patient, vitals, visit, consults, prescriptions)
