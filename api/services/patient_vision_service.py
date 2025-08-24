from typing import Optional
from django.shortcuts import get_object_or_404
from api.models import Visit, Patient, Vitals, Glasses
from api.viewmodels.patient_vision_viewmodel import PatientVisionViewModel

_VITAL_PICK = (
    "id", "visit_id",
    "right_eye_degree", "left_eye_degree",
    "right_eye_pinhole", "left_eye_pinhole",
)

def get_patient_vision_viewmodel(visit_id: int) -> PatientVisionViewModel:
    """
      - patient: full Patient
      - vision : latest Glasses for the visit (full) or None
      - vitals : dict with only the 4 requested fields or None
    """
    visit = get_object_or_404(
        Visit.objects.select_related("patient").only("id", "patient_id", "date"),
        pk=visit_id,
    )

    patient_qs = (
        Patient.objects
    )
    patient: Patient = patient_qs.get(pk=visit.patient_id)

    glasses_qs = (
        Glasses.objects.filter(visit_id=visit_id)
        .order_by("-id")
    )
    vision: Optional[Glasses] = glasses_qs.first()

    vitals: Optional[Vitals] = (
        Vitals.objects.filter(visit_id=visit_id)
        .only(*_VITAL_PICK)
        .order_by("-id")
        .first()
    )

    vitals_dict = None
    if vitals:
        vitals_dict = {
            "right_eye_degree":  getattr(vitals, "right_eye_degree", None),
            "left_eye_degree":   getattr(vitals, "left_eye_degree", None),
            "right_eye_pinhole": getattr(vitals, "right_eye_pinhole", None),
            "left_eye_pinhole":  getattr(vitals, "left_eye_pinhole", None),
        }

    return PatientVisionViewModel(patient=patient, vision=vision, vitals=vitals_dict)
