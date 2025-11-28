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
    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")

    # Edge case - missing consult_id
    missing_consult_data = payload.copy()
    del missing_consult_data["consult_id"]
    response = api_client.post(
        reverse("diagnosis:diagnosis_list"), missing_consult_data
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")
    assert response.data["error"].find("consult") != -1

    # Edge case - invalid consult_id
    invalid_consult_data = dict(payload)
    invalid_consult_data["consult_id"] = "invalid_id"
    response = api_client.post(
        reverse("diagnosis:diagnosis_list"), invalid_consult_data
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Invalid")
    assert response.data["error"].find("consult") != -1

    # Edge case - Nonexistent consult_id
    nonexistent_consult_data = dict(payload)
    nonexistent_consult_data["consult_id"] = 99999
    response = api_client.post(
        reverse("diagnosis:diagnosis_list"), nonexistent_consult_data
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Cannot find")
    assert response.data["error"].find("consult") != -1

    # Edge case - Missing details error
    missing_details_data = payload.copy()
    del missing_details_data["details"]
    response = api_client.post(
        reverse("diagnosis:diagnosis_list"), missing_details_data
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")
    assert response.data["error"].find("details") != -1

    # Edge case - Missing category error
    missing_category_data = payload.copy()
    del missing_category_data["category"]
    response = api_client.post(
        reverse("diagnosis:diagnosis_list"), missing_category_data
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")
    assert response.data["error"].find("category") != -1


@pytest.mark.django_db
def test_diagnosis_get_one(api_client, diagnosis_instance):
    """Test retrieving diagnoses via GET - single"""
    # Successful case - retrieve single diagnosis by pk
    response = api_client.get(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_instance.pk)])
    )
    assert response.status_code == 200
    expected = DiagnosisSerializer(diagnosis_instance).data
    assert response.data == expected

    # Edge case - get nonexistent diagnosis
    response = api_client.get(reverse("diagnosis:diagnosis_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_diagnosis_get_list(api_client, diagnosis_instance, consult):
    """Test retrieving diagnoses via GET - list by consult"""
    # Successful case - list diagnoses
    response = api_client.get(reverse("diagnosis:diagnosis_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == diagnosis_instance.id

    # Successful case - list diagnoses by consult
    response = api_client.get(
        reverse("diagnosis:diagnosis_list") + f"?consult={consult.id}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == diagnosis_instance.pk
    assert response.data[0]["consult"] == consult.pk

    # Edge case - list diagnoses by nonexistent consult
    response = api_client.get(reverse("diagnosis:diagnosis_list") + "?consult=99999")
    assert response.status_code == 200
    assert len(response.data) == 0

    # Edge case - list diagnoses by invalid consult
    response = api_client.get(reverse("diagnosis:diagnosis_list") + "?consult='123'")
    assert response.status_code == 400
    assert response.data["error"].startswith("Invalid")
    assert response.data["error"].find("consult") != -1


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

    # Edge case - update nonexistent diagnosis - fail
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=["99999"]), diagnosis_data
    )
    assert response.status_code == 404
    assert response.data["error"].startswith("Cannot find")
    assert response.data["error"].find("diagnosis") != -1

    # Edge case - update diagnosis with non-existent consult_id - fail
    invalid_consult_data = dict(diagnosis_data)
    invalid_consult_data["consult_id"] = 99999
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_instance.pk)]),
        invalid_consult_data,
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Cannot find")
    assert response.data["error"].find("consult") != -1


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
