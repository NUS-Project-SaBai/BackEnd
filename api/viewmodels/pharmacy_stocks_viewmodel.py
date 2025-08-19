from dataclasses import dataclass

@dataclass
class MedicationHistoryVM:
    approval_name: str
    doctor_name: str
    patient_name: str
    qty_changed: int
    qty_remaining: int
    date: str

@dataclass
class PharmacyStockVM:
    medicine_id: int
    medicine_name: str
    quantity: int
    code: str