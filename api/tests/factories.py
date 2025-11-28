"""
Simplified test factories: return the dummy payloads as-is and provide
batch ORM creators that create database records in the same order as the
numbered dummies. This keeps tests using the raw dummy data without
mixing values from a separate base dummy.
"""

from datetime import datetime
from typing import Dict, Any, List

from django.utils import timezone

import api.tests.dummies as dummy
from api.models import Patient, Visit, Consult, Medication


def _collect(prefix: str, **overrides) -> List[Dict[str, Any]]:
    """
    Collect dummy dicts from the `dummy` module whose names start with `prefix`,
    ordered lexicographically (which matches numeric suffix ordering for our names like
    post_x_dummy_1, _2...). Apply any overrides to each dummy.


    Args:
        prefix (str): The prefix to filter dummy names.
        **overrides: Key-value pairs to override in each dummy. None will remove the key.
    Returns:
        List[Dict[str, Any]]: List of dummy dicts with applied overrides.

    """
    names = sorted([n for n in dir(dummy) if n.startswith(prefix)])
    # Return a copy of each dummy to avoid mutating the original
    dummies: list[dict] = [getattr(dummy, n).copy() for n in names]
    if overrides:
        for d in dummies:
            for key, value in overrides.items():
                if value is None:
                    d.pop(key, None)
                else:
                    d[key] = value
    return dummies


# Payload accessors (return the dummies "as-is", applying any overrides to all)
def patient_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_patient_dummy", **overrides)


def visit_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_visit_dummy", **overrides)


def consult_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_consult_dummy", **overrides)


def diagnosis_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_diagnosis_dummy", **overrides)


def medication_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_medication_dummy", **overrides)


def order_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_order_dummy", **overrides)


def vitals_payloads(**overrides) -> List[Dict[str, Any]]:
    return _collect("post_vitals_dummy", **overrides)


# ORM batch creators that create objects using the dummy payloads in order
# and map dummy numeric ids (1-based) to created objects by index.


def _parse_date_or_now(value: Any):
    if not value:
        return timezone.now()
    try:
        return timezone.make_aware(datetime.fromisoformat(value))
    except Exception:
        return timezone.now()


def create_patients_from_dummies() -> List[Patient]:
    created: List[Patient] = []
    for payload in patient_payloads():
        dob = payload.get("date_of_birth")
        patient = Patient.objects.create(
            village_prefix=payload.get("village_prefix"),
            name=payload.get("name"),
            identification_number=payload.get("identification_number"),
            contact_no=payload.get("contact_no"),
            gender=payload.get("gender"),
            date_of_birth=_parse_date_or_now(dob),
            drug_allergy=payload.get("drug_allergy"),
            face_encodings=payload.get("face_encodings", ""),
            picture=payload.get("picture"),
        )
        created.append(patient)
    return created


def create_visits_from_dummies(patients: List[Patient]) -> List[Visit]:
    """Create visits using `visit_payloads`. Each visit dummy contains a
    `patient_id` that corresponds to the dummy patient numeric id (1-based).
    We map that to the created `patients` list by index: dummy patient_id 1
    -> patients[0]."""
    created: List[Visit] = []
    for payload in visit_payloads():
        dummy_patient_id = payload.get("patient_id", 1)
        # Map to created patients list (1-based to 0-based)
        try:
            patient = patients[int(dummy_patient_id) - 1]
        except Exception:
            patient = patients[0]
        visit = Visit.objects.create(
            patient=patient,
            date=_parse_date_or_now(payload.get("date")),
            status=payload.get("status"),
        )
        created.append(visit)
    return created


def create_consults_from_dummies(visits: List[Visit]) -> List[Consult]:
    created: List[Consult] = []
    for payload in consult_payloads():
        dummy_visit_id = payload.get("visit_id")
        try:
            visit = visits[int(dummy_visit_id) - 1]
        except Exception:
            visit = visits[0]
        consult = Consult.objects.create(
            visit=visit,
            date=_parse_date_or_now(payload.get("date")),
            doctor_id=payload.get("doctor_id"),
            past_medical_history=payload.get("past_medical_history"),
            consultation=payload.get("consultation"),
            plan=payload.get("plan"),
            referred_for=payload.get("referred_for"),
            referral_notes=payload.get("referral_notes"),
            remarks=payload.get("remarks"),
        )
        created.append(consult)
    return created


def create_medications_from_dummies() -> List[Consult]:
    """Create medications using `medication_payloads`."""
    created: List[Consult] = []
    for payload in medication_payloads():
        medication = Medication.objects.create(**payload)
        created.append(medication)
    return created
