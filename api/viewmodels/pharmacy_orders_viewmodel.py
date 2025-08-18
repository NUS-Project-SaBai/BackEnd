from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass(frozen=True)
class PharmacyOrderVM:
    id: int
    medication_name: Optional[str]
    medication_code: Optional[str]
    quantity_changed: Optional[int]
    notes: Optional[str]

@dataclass(frozen=True)
class DiagnosisVM:
    category: str
    details: str

@dataclass(frozen=True)
class VisitBundleVM:
    visit_id: int
    visit_date: Optional[datetime]
    orders: List[PharmacyOrderVM]
    diagnoses: List[DiagnosisVM]

@dataclass(frozen=True)
class PatientHeaderVM:
    patient_id: str
    name: str
    picture_url: Optional[str]
    village_prefix: str

@dataclass(frozen=True)
class PharmacyPatientBundleVM:
    patient: PatientHeaderVM
    data: List[VisitBundleVM]
