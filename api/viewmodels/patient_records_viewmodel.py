class PatientRecordViewModel:
    def __init__(self, patient, vitals, visit, consults, prescriptions):
        self.patient = patient
        self.vitals = vitals
        self.visit_date = visit.date
        self.consults = consults
        self.prescriptions = [
            {
                "consult_id": order.consult_id,
                "visit_date": order.consult.visit.date,
                "medication": (
                    order.medication_review.medicine.medicine_name
                    if order.medication_review and order.medication_review.medicine
                    else None
                ),
                "quantity": (
                    order.medication_review.quantity_changed
                    if order.medication_review
                    else None
                ),
                "notes": order.notes,
                "status": (
                    order.medication_review.order_status
                    if order.medication_review
                    else "UNKNOWN"
                ),
            }
            for order in prescriptions
        ]
