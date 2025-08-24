def _med_name(med) -> str | None:
    if med is None:
        return None
    # works whether field is "medicine_name" or "name"
    return getattr(med, "medicine_name", None) or getattr(med, "name", None)

class PatientConsultViewModel:
    """
    Shapes to FE spec:
      - patient: full Patient
      - vitals: full Vitals
      - visit_date: ISO-able date
      - consults: [{id, date, doctor:{nickname}, referred_for}]
      - prescriptions: [{consult_id, visit_date, medication, quantity, notes, status}]
    """
    def __init__(self, patient, vitals, visit, consults, orders):
        self.patient = patient
        self.vitals = vitals
        self.visit_date = visit.date

        self.consults = [
            {
                "id": c.id,
                "date": c.date,
                "doctor": {"nickname": getattr(getattr(c, "doctor", None), "nickname", None)},
                "referred_for": getattr(c, "referred_for", None),
            }
            for c in consults
        ]

        self.prescriptions = []
        for o in orders:
            mr = getattr(o, "medication_review", None)
            med = getattr(mr, "medicine", None) if mr else None
            self.prescriptions.append({
                "consult_id": getattr(o, "consult_id", None),
                "visit_date": (
                    getattr(getattr(getattr(o, "consult", None), "visit", None), "date", None)
                ),
                "medication": _med_name(med),
                "quantity": getattr(mr, "quantity_changed", None) if mr else None,
                "notes": getattr(o, "notes", None),
                "status": getattr(mr, "order_status", None) if mr else "UNKNOWN",
            })
