"""
Pytest-style version of test_post_all.py
"""
import pytest
from django.urls import reverse

import api.tests.dummies as dummy
from api.tests.factories import (
    patient_payloads,
    visit_payloads,
    vitals_payloads,
    diagnosis_payloads,
    medication_payloads,
    order_payloads,
)
from api.tests.factories import consult_payloads


@pytest.mark.django_db
def test_post_all_endpoints(api_client, test_user):
    """Test creating all entities in sequence (patient, visit, vitals, consult, diagnosis, medication, order)"""
    patient_payload = patient_payloads()[0]
    visit_payload = visit_payloads()[0]
    vitals_payload = vitals_payloads()[0]
    consult_payload = consult_payloads()[0]
    diagnosis_payload = diagnosis_payloads()[0]
    medication_payload = medication_payloads()[0]
    order_payload = order_payloads()[0]
    # Create patient
    create_patient = api_client.post(
        reverse("patients:patients_list"), patient_payloads()[0]
    )
    assert create_patient.status_code == 200

    # Create visit
    create_visit = api_client.post(reverse("visits:visits_list"), visit_payload)
    assert create_visit.status_code == 200

    # Create vitals
    create_vitals = api_client.post(reverse("vitals:vitals_list"), vitals_payload)
    assert create_vitals.status_code == 200

    # Create consult with doctor header
    create_consult = api_client.post(
        reverse("consults:consults_list"),
        {"consult": consult_payload},
        headers={"doctor": test_user.email},
    )
    assert create_consult.status_code == 201

    # Create diagnosis
    create_diagnosis = api_client.post(
        reverse("diagnosis:diagnosis_list"), diagnosis_payload
    )
    assert create_diagnosis.status_code == 201

    # Create medication with doctor header
    create_medication = api_client.post(
        reverse("medication:medications_list"),
        medication_payload,
        headers={"doctor": test_user.email},
    )
    assert create_medication.status_code == 201

    # Create order
    create_order = api_client.post(reverse("orders:orders_list"), order_payload)
    assert create_order.status_code == 201
