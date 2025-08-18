from dataclasses import dataclass

@dataclass
class MedicationHistoryVM:
    approval_name: str
    doctor_name: str
    patient_name: str
    qty_changed: int
    qty_remaining: int
    date: str
