"""
Test diagnosis API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Diagnosis
from api.serializers import DiagnosisSerializer
import api.tests.dummies as dummy
from api.tests.factories import diagnosis_payloads


@pytest.fixture
def diagnosis_instance(api_client, consult):
    """Create a diagnosis instance for tests that need existing data"""
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.post(reverse("diagnosis:diagnosis_list"), diagnosis_data)
    assert response.status_code == 201
    return Diagnosis.objects.get(pk=response.data["id"])


@pytest.mark.django_db
def test_diagnosis_post(api_client, consult):
    """Test creating diagnoses via POST - success and edge cases"""
    # Successful case - create diagnosis
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.post(reverse("diagnosis:diagnosis_list"), diagnosis_data)
    assert response.status_code == 201
    expected = DiagnosisSerializer(Diagnosis.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty diagnosis data
    response = api_client.post(reverse("diagnosis:diagnosis_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation


@pytest.mark.django_db
def test_diagnosis_get(api_client, diagnosis_instance):
    """Test retrieving diagnoses via GET - single, list, and edge cases"""
    # Successful case - retrieve single diagnosis by pk
    response = api_client.get(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_instance.pk)])
    )
    assert response.status_code == 200
    expected = DiagnosisSerializer(diagnosis_instance).data
    assert response.data == expected

    # Successful case - list diagnoses
    response = api_client.get(reverse("diagnosis:diagnosis_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == diagnosis_instance.pk

    # Edge case - get nonexistent diagnosis
    response = api_client.get(reverse("diagnosis:diagnosis_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_diagnosis_patch(api_client, diagnosis_instance, consult):
    """Test updating diagnoses via PATCH - success and edge cases"""
    # Successful case - update diagnosis
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_instance.pk)]),
        diagnosis_data,
    )
    assert response.status_code == 200
    expected = DiagnosisSerializer(diagnosis_instance).data
    assert response.data == expected

    # Edge case - update nonexistent diagnosis
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=["99999"]), diagnosis_data
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_diagnosis_delete(api_client, diagnosis_instance):
    """Test deleting diagnoses via DELETE - success and edge cases"""
    diagnosis_pk = diagnosis_instance.pk

    # Successful case - delete diagnosis
    response = api_client.delete(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_pk)])
    )
    assert response.status_code == 204
    assert response.data == {"message": "Deleted successfully"}

    # Verify diagnosis is gone from list
    response = api_client.get(reverse("diagnosis:diagnosis_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted diagnosis (should 404)
    response = api_client.delete(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_pk)])
    )
    assert response.status_code == 404

    # Edge case - delete nonexistent diagnosis
    response = api_client.delete(reverse("diagnosis:diagnosis_pk", args=["99999"]))
    assert response.status_code == 404
