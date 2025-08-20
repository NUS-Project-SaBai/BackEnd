class MedicationHistoryVM:
    def __init__(self, review, visit, doctor):
        self.approval_name = getattr(review.approval, "name", "-") if review.approval else "-"
        self.doctor_name = doctor.nickname if doctor else "-"
        self.patient_name = visit.patient.name if visit and visit.patient else "-"
        self.qty_changed = review.quantity_changed
        self.qty_remaining = review.quantity_remaining
        self.date = review.date.isoformat() if review.date else None
