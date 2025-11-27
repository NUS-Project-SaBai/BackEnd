"""
Pytest-style version of test_post_all.py
"""
import pytest
from django.urls import reverse

import api.tests.dummy as dummy


@pytest.mark.django_db
def test_post_all_endpoints(api_client, test_user):
    """Test creating all entities in sequence (patient, visit, vitals, consult, diagnosis, medication, order)"""
    # Create patient
    create_patient = api_client.post(reverse("patients:patients_list"), dummy.post_patient_dummy)
    assert create_patient.status_code == 200

    # Create visit
    create_visit = api_client.post(reverse("visits:visits_list"), dummy.post_visit_dummy)
    assert create_visit.status_code == 200

    # Create vitals
    create_vitals = api_client.post(reverse("vitals:vitals_list"), dummy.post_vitals_dummy)
    assert create_vitals.status_code == 200

    # Create consult with doctor header
    create_consult = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
        HTTP_DOCTOR=test_user.email,
    )
    assert create_consult.status_code == 201

    # Create diagnosis
    create_diagnosis = api_client.post(reverse("diagnosis:diagnosis_list"), dummy.post_diagnosis_dummy)
    assert create_diagnosis.status_code == 201

    # Create medication with doctor header
    create_medication = api_client.post(
        reverse("medication:medications_list"),
        dummy.post_medication_dummy,
        HTTP_DOCTOR=test_user.email,
    )
    assert create_medication.status_code == 201

    # Create order
    create_order = api_client.post(reverse("orders:orders_list"), dummy.post_order_dummy)
    assert create_order.status_code == 201
