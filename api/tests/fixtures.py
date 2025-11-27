"""
Common model fixtures for tests.
Centralizes patient, visit, and other model creation to avoid duplication.
"""

import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient, Visit
import api.tests.dummies as dummy


@pytest.fixture
def patient(db):
    """Create a test patient using dummy data"""
    return Patient.objects.create(
        village_prefix=dummy.post_patient_dummy.get("village_prefix", "VPF"),
        name=dummy.post_patient_dummy.get("name", "patient_name"),
        identification_number=dummy.post_patient_dummy.get("identification_number"),
        contact_no=dummy.post_patient_dummy.get("contact_no"),
        gender=dummy.post_patient_dummy.get("gender", "gender"),
        date_of_birth=timezone.make_aware(
            datetime.fromisoformat(dummy.post_patient_dummy.get("date_of_birth"))
        ),
        drug_allergy=dummy.post_patient_dummy.get("drug_allergy", "drug_allergy"),
        face_encodings=dummy.post_patient_dummy.get("face_encodings", ""),
        picture=dummy.post_patient_dummy.get("picture", "image/upload/v1/dummy.jpg"),
    )


@pytest.fixture
def visit(patient):
    """Create a test visit using dummy data"""
    return Visit.objects.create(
        patient=patient,
        date=timezone.make_aware(
            datetime.fromisoformat(dummy.post_visit_dummy.get("date"))
        ),
        status=dummy.post_visit_dummy.get("status"),
    )


@pytest.fixture
def consult(api_client, patient, visit):
    """Create a consult instance for tests"""
    data = {**dummy.post_consult_dummy, "patient": patient.id, "visit": visit.id}
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": data},
        headers={"doctor": "test@example.com"},
    )
    assert response.status_code == 201
    return response.data["id"]


@pytest.fixture
def consult_and_medication(api_client, consult):
    """Create consult and medication for order tests"""
    # Create medication
    response_med = api_client.post(
        reverse("medication:medications_list"),
        dummy.post_medication_dummy,
        headers={"doctor": "test@example.com"},
    )
    assert response_med.status_code == 201
    medication_id = response_med.data["id"]
    return consult, medication_id


@pytest.fixture
def patient_and_visit(api_client):
    """Create patient and visit for vitals tests"""
    # Create patient
    response_patient = api_client.post(
        reverse("patients:patients_list"), dummy.post_patient_dummy
    )
    assert response_patient.status_code == 200
    patient_id = 1  # Assume first patient

    # Create visit
    visit_data = {**dummy.post_visit_dummy, "patient": patient_id}
    response_visit = api_client.post(reverse("visits:visits_list"), visit_data)
    assert response_visit.status_code == 200
    visit_id = response_visit.data["id"]

    return patient_id, visit_id
