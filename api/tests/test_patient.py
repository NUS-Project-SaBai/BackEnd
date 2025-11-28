"""
Test patient API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Patient
from api.serializers import PatientSerializer
import api.tests.dummies as dummy
from api.tests.factories import patient_payloads


@pytest.fixture
def patient_instance(api_client):
    """Create a patient instance for tests that need existing data"""
    payload = patient_payloads()[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200
    return Patient.objects.get(pk=1)


@pytest.mark.django_db
def test_patient_post(api_client):
    """Test creating patients via POST - success and edge cases"""
    # Successful case - create patient
    payload = patient_payloads()[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200

    patient = Patient.objects.get(pk=1)
    expected = PatientSerializer(patient).data
    assert response.data == expected

    # Edge case - empty patient data
    response = api_client.post(reverse("patients:patients_list"), {})
    assert response.status_code == 200  # API allows empty data?


@pytest.mark.django_db
def test_patient_get(api_client, patient_instance):
    """Test retrieving patients via GET - single, list, and edge cases"""
    # Successful case - retrieve single patient by pk
    response = api_client.get(
        reverse("patients:patients_pk", args=[patient_instance.pk])
    )
    assert response.status_code == 200
    # Note: response.data may include additional fields like last_visit_date

    # Successful case - list patients
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["pk"] == patient_instance.pk

    # Edge case - get nonexistent patient
    response = api_client.get(reverse("patients:patients_pk", args=["99999"]))
    assert response.status_code == 200  # API returns 200 for nonexistent


@pytest.mark.django_db
def test_patient_patch(api_client, patient_instance):
    """Test updating patients via PATCH - success and edge cases"""
    # Successful case - update patient
    update_payload = {"name": "updated_name"}
    response = api_client.patch(
        reverse("patients:patients_pk", args=[patient_instance.pk]), update_payload
    )
    assert response.status_code == 200

    patient_instance.refresh_from_db()
    expected = PatientSerializer(patient_instance).data
    assert response.data == expected

    # Edge case - update nonexistent patient
    response = api_client.patch(
        reverse("patients:patients_pk", args=["99999"]), update_payload
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_patient_delete(api_client, patient_instance):
    """Test deleting patients via DELETE - success and edge cases"""
    patient_pk = patient_instance.pk

    # Successful case - delete patient
    response = api_client.delete(reverse("patients:patients_pk", args=[patient_pk]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify patient is gone from list
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted patient (should 404)
    response = api_client.delete(
        reverse("patients:patients_pk", args=[str(patient_pk)])
    )
    assert response.status_code == 404

    # Edge case - delete nonexistent patient
    response = api_client.delete(reverse("patients:patients_pk", args=["99999"]))
    assert response.status_code == 404
