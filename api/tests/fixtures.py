"""
Common model fixtures for tests.
Centralizes patient, visit, and other model creation to avoid duplication.
"""

import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient, Visit, Consult
import api.tests.dummies as dummy
from api.tests.factories import (
    patient_payloads,
    visit_payloads,
    consult_payloads,
    diagnosis_payloads,
    medication_payloads,
    order_payloads,
    vitals_payloads,
    create_patients_from_dummies,
    create_visits_from_dummies,
    create_consults_from_dummies,
)


# ----------------------
# Core ORM fixtures
# ----------------------


@pytest.fixture
def all_dummy_patients(db):
    """Create and return patient objects created from the numbered dummies."""
    return create_patients_from_dummies()


@pytest.fixture
def patient(all_dummy_patients):
    """Return the first dummy patient."""
    return all_dummy_patients[0]


@pytest.fixture
def all_dummy_visits(all_dummy_patients):
    """Create visits from dummies mapped to the created patients."""
    return create_visits_from_dummies(all_dummy_patients)


@pytest.fixture
def visit(all_dummy_visits):
    """Return the first dummy visit."""
    return all_dummy_visits[0]


# Provide a convenience fixture that creates a consult via API and returns the ORM instance.
@pytest.fixture
def consult(api_client, visit, test_user):
    base = consult_payloads()[0]
    data = {**base, "patient": visit.patient.id, "visit": visit.id}
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": data},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    return Consult.objects.get(pk=response.data["id"])


# ----------------------
# API resource fixtures
# ----------------------


@pytest.fixture
def consult_id(api_client, patient, visit):
    """Create a consult via API and return its id"""
    base = consult_payloads()[0]
    data = {**base, "patient": patient.id, "visit": visit.id}
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": data},
        headers={"doctor": "test@example.com"},
    )
    assert response.status_code == 201
    return response.data["id"]


@pytest.fixture
def consult_and_medication(api_client, visit, consult_factory):
    """Create consult and medication via API for order tests"""
    # Create consult via provided factory
    consult_id = consult_factory(visit.patient.id, visit.id)

    # Create medication
    response_med = api_client.post(
        reverse("medication:medications_list"),
        medication_payloads()[0],
        headers={"doctor": "test@example.com"},
    )
    assert response_med.status_code == 201
    medication_id = response_med.data["id"]
    return consult_id, medication_id


@pytest.fixture
def patient_and_visit(api_client):
    """Create patient and visit via API for vitals tests"""
    # Create patient
    patient_payload = patient_payloads()[0]
    response_patient = api_client.post(
        reverse("patients:patients_list"), patient_payload
    )
    assert response_patient.status_code == 200
    patient_id = 1  # Assume first patient

    # Create visit
    visit_data = dict(visit_payloads()[0])
    visit_data["patient_id"] = patient_id
    response_visit = api_client.post(reverse("visits:visits_list"), visit_data)
    assert response_visit.status_code == 200
    visit_id = response_visit.data["id"]

    return patient_id, visit_id


# ----------------------
# Additional ORM test data
# ----------------------


@pytest.fixture
def patients_many(db):
    """Create multiple patients for list/filter tests"""
    patients = create_patients_from_dummies()
    return patients[:3]


@pytest.fixture
def visit_factory(db):
    """Simple factory function to create visits for a patient."""

    def _create(patient, days_offset=0, status="open"):
        return Visit.objects.create(
            patient=patient,
            date=timezone.now(),
            status=status,
        )

    return _create


@pytest.fixture
def medication_api(api_client):
    """Create a medication via API and return its id"""
    payload = medication_payloads()[0]
    response = api_client.post(
        reverse("medication:medications_list"),
        payload,
        headers={"doctor": "test@example.com"},
    )
    assert response.status_code in (200, 201)
    return response.data["id"]


@pytest.fixture
def consult_factory(api_client):
    """Factory function to create consults via API (requires doctor header)"""

    def _create(patient_id, visit_id, overrides=None):
        base = consult_payloads()[0]
        data = {**base, "patient": patient_id, "visit": visit_id}
        if overrides:
            data.update(overrides)
        response = api_client.post(
            reverse("consults:consults_list"),
            {"consult": data},
            headers={"doctor": "test@example.com"},
        )
        assert response.status_code == 201
        return response.data["id"]

    return _create


@pytest.fixture
def full_patient_setup(api_client):
    """Create patient, visit, consult and medication via API and return ids"""

    def _create():
        # patient
        patient_payload = patient_payloads()[0]
        resp_p = api_client.post(reverse("patients:patients_list"), patient_payload)
        assert resp_p.status_code in (200, 201)
        patient_id = resp_p.data.get("id", 1)

        # visit
        visit_data = dict(visit_payloads()[0])
        visit_data["patient_id"] = patient_id
        resp_v = api_client.post(reverse("visits:visits_list"), visit_data)
        assert resp_v.status_code in (200, 201)
        visit_id = resp_v.data["id"]

        # consult
        consult_resp = api_client.post(
            reverse("consults:consults_list"),
            {
                "consult": {
                    **consult_payloads()[0],
                    "patient": patient_id,
                    "visit": visit_id,
                }
            },
            headers={"doctor": "test@example.com"},
        )
        assert consult_resp.status_code == 201
        consult_id = consult_resp.data["id"]

        # medication
        med_payload = medication_payloads()[0]
        med_resp = api_client.post(
            reverse("medication:medications_list"),
            med_payload,
            headers={"doctor": "test@example.com"},
        )
        assert med_resp.status_code in (200, 201)
        medication_id = med_resp.data["id"]

        return {
            "patient_id": patient_id,
            "visit_id": visit_id,
            "consult_id": consult_id,
            "medication_id": medication_id,
        }

    return _create
