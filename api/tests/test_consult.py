"""
Test consult API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

import api.tests.dummies as dummy
from api.tests.factories import consult_payloads
from api.models import Consult
from api.serializers import ConsultSerializer


@pytest.mark.django_db
def test_consult_post(api_client, visit, test_user):
    """Test creating consults via POST - success and edge cases"""
    payload = consult_payloads()[0]
    # Successful case - create consult
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": payload},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201

    consult = Consult.objects.get(pk=1)
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - missing required doctor header
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": payload},
    )
    assert response.status_code == 400

    # Edge case - empty consult data
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": {}},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 400

    # Edge case - missing visit_id
    missing_visit_dummy = dict(payload)
    del missing_visit_dummy["visit_id"]
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": missing_visit_dummy},
        headers={"doctor": test_user.email},
    )

    assert (
        response.data.get("error", None) is not None
        and response.status_code == 400
        and response.data["error"].startswith("Missing")
        and response.data["error"].find("visit_id") != -1
    )

    # Edge case - invalid visit_id
    invalid_visit_dummy = dict(payload)
    invalid_visit_dummy["visit_id"] = "invalid_id"
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": invalid_visit_dummy},
        headers={"doctor": test_user.email},
    )
    assert (
        response.status_code == 400
        and response.data.get("error", None) is not None
        and response.data["error"].startswith("Invalid")
        and response.data["error"].find("visit_id") != -1
    )

    # Edge case - nonexistent visit_id
    nonexistent_visit_dummy = dict(payload)
    nonexistent_visit_dummy["visit_id"] = 99999
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": nonexistent_visit_dummy},
        headers={"doctor": test_user.email},
    )
    assert (
        response.status_code == 400
        and response.data.get("error", None) is not None
        and response.data["error"].startswith("Cannot find")
        and response.data["error"].find("visit_id") != -1
    )


@pytest.mark.django_db
def test_consult_get_pk(api_client, consult):
    """Test retrieving consults via GET - single"""
    # Successful case - retrieve single consult by pk
    response = api_client.get(reverse("consults:consults_pk", args=[str(consult.pk)]))
    assert response.status_code == 200
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - get nonexistent consult
    response = api_client.get(reverse("consults:consults_pk", args=["99999"]))
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )


@pytest.mark.django_db
def test_consult_get_all(api_client, consult):
    """Test retrieving consults via GET - list all"""
    # Successful case - list all consults
    response = api_client.get(reverse("consults:consults_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == consult.pk


@pytest.mark.django_db
def test_consult_get_visit(api_client, consult, visit):
    """Test retrieving consults via GET - list"""
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
def test_consult_get_patient(api_client, consult, visit):
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


@pytest.mark.django_db
def test_consult_patch(api_client, consult, test_user):
    """Test updating consults via PATCH - success and edge cases"""
    payload = consult_payloads()[0]
    # Successful case - update consult
    updated_dummy = dict(payload)
    response = api_client.patch(
        reverse("consults:consults_pk", args=[str(consult.pk)]),
        {"consult": updated_dummy},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 200

    consult.refresh_from_db()
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - update nonexistent consult
    response = api_client.patch(
        reverse("consults:consults_pk", args=["99999"]),
        {"consult": updated_dummy},
        headers={"doctor": test_user.email},
    )
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )


@pytest.mark.django_db
def test_consult_delete(api_client, consult):
    """Test deleting consults via DELETE - success and edge cases"""
    visit_id = consult.visit.pk
    consult_id = consult.pk

    # Successful case - delete consult
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_id)])
    )
    assert response.status_code == 204
    assert response.data == {"message": "Deleted successfully"}

    # Verify consult is gone from list
    response = api_client.get(
        reverse("consults:consults_list") + f"?visit_id={visit_id}"
    )
    assert response.status_code == 200
    assert response.data == []

    response = api_client.get(reverse("consults:consults_pk", args=[str(consult_id)]))
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )

    # Edge case - delete already deleted consult (should 404)
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_id)])
    )
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )

    # Edge case - delete nonexistent consult
    response = api_client.delete(reverse("consults:consults_pk", args=["99999"]))
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )
