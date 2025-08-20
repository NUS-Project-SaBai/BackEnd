class MedicationHistoryVM:
    def __init__(self, review, consult):
        self.approval_name = getattr(review.approval, "name", "-") if review.approval else "-"
        self.doctor_name = consult.doctor.nickname if consult and consult.doctor else "-"
        self.patient_name = consult.visit.patient.name if consult and consult.visit and consult.visit.patient else "-"
        self.qty_changed = review.quantity_changed
        self.qty_remaining = review.quantity_remaining
        self.date = review.date.isoformat() if review.date else None
