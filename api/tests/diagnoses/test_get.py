"""
GET tests for diagnoses
"""

import pytest
from rest_framework.reverse import reverse

from api.serializers import DiagnosisSerializer


@pytest.mark.django_db
def test_diagnoses_get_Single(api_client, diagnosis_instance):
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
def test_diagnoses_get_ListAndFilters(api_client, diagnosis_instance, consult):
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
