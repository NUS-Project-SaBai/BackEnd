class MedicationHistoryViewModel:
    def __init__(self, medication_review, consult):
        self.approval_name = (
            getattr(medication_review.approval, "name", "-")
            if medication_review.approval
            else "-"
        )
        self.doctor_name = (
            consult.doctor.nickname if consult and consult.doctor else "-"
        )
        self.patient_name = (
            consult.visit.patient.name
            if consult and consult.visit and consult.visit.patient
            else "-"
        )
        self.qty_changed = medication_review.quantity_changed
        self.qty_remaining = medication_review.quantity_remaining
        self.date = (
            medication_review.date.isoformat() if medication_review.date else None
        )
