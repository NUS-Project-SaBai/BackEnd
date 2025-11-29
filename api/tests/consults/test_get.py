"""
GET tests for consults
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Consult
from api.serializers import ConsultSerializer


@pytest.mark.django_db
def test_consults_get_Single(api_client, consult):
    """Test retrieving consults via GET - single"""
    # Successful case - retrieve single consult by pk
    response = api_client.get(reverse("consults:consults_pk", args=[str(consult.pk)]))
    assert response.status_code == 200
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - get nonexistent consult
    response = api_client.get(reverse("consults:consults_pk", args=["99999"]))
    assert response.status_code == 404
    assert response.data.get("error") == "Consult not found"


@pytest.mark.django_db
def test_consults_get_ListAll(api_client, consult):
    """Test retrieving consults via GET - list all"""
    # Successful case - list all consults
    response = api_client.get(reverse("consults:consults_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == consult.pk


@pytest.mark.django_db
def test_consults_get_ByVisit(api_client, consult, visit):
    """Test retrieving consults via GET - list by visit"""
    # Successful case - list consults by visit
    response = api_client.get(
        reverse("consults:consults_list") + f"?visit_id={consult.visit.id}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == consult.pk

    # Edge case - list consults by visit with no consults, valid but empty list
    response = api_client.get(reverse("consults:consults_list") + f"?visit_id=99999")
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_consults_get_ByPatient(api_client, consult, visit):
    """Test retrieving consults via GET - list by patient_id"""
    # Successful case - list consults by patient_id
    response = api_client.get(
        reverse("consults:consults_list") + f"?patient_id={visit.patient.pk}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == consult.pk

    # Edge case - list consults by patient_id (no consults)
    response = api_client.get(reverse("consults:consults_list") + f"?patient_id=99999")
    assert response.status_code == 200
    assert response.data == []
