class PharmacyOrderVM:
    def __init__(self, order):
        medicine = order.medication_review.medicine if order.medication_review else None
        self.order_id = order.id
        self.medication_name = medicine.medicine_name if medicine else None
        self.medication_code = medicine.code if medicine else None
        self.quantity_changed = (
            order.medication_review.quantity_changed
            if order.medication_review
            else None
        )
        self.is_low_stock = (
            medicine.warning_quantity != None
            and medicine.quantity < medicine.warning_quantity
        )
        self.notes = order.notes


class DiagnosisVM:
    def __init__(self, diagnosis):
        self.category = diagnosis.category
        self.details = diagnosis.details


class VisitBundleVM:
    def __init__(self, visit, orders, diagnoses):
        self.visit_id = visit.pk
        self.visit_date = visit.date
        self.orders = orders
        self.diagnoses = diagnoses


class PatientHeaderVM:
    def __init__(self, patient):
        self.patient_id = getattr(patient, "patient_id", str(patient.pk))
        self.name = getattr(patient, "name", str(patient))
        self.picture_url = getattr(getattr(patient, "picture", None), "url", None)
        self.village_prefix = str(getattr(patient, "village_prefix", "")) or ""


class PharmacyPatientBundleVM:
    def __init__(self, patient, data):
        self.patient = patient
        self.data = data
