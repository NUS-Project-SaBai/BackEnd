"""
Test consult API endpoints - organized by HTTP method with edge cases
"""

from typing import Iterable
import pytest
from rest_framework.reverse import reverse

import api.tests.dummies as dummy
from api.tests.factories import consult_payloads, order_payloads, diagnosis_payloads
from api.models import Consult, Diagnosis, Order
from api.serializers import ConsultSerializer


def create_consult_payload(visit_id, include_orders=True, include_diagnoses=True):
    """Helper to create a consult payload with given visit_id"""
    payload = {}
    payload["consult"] = consult_payloads()[0].copy()
    if include_orders:
        payload["orders"] = order_payloads(consult_id=None)
    if include_diagnoses:
        payload["diagnoses"] = diagnosis_payloads(consult_id=None).copy()
    payload["visit_id"] = visit_id
    return payload


@pytest.mark.django_db
def test_consult_post(api_client, visit, test_user):
    """Test creating consults via POST - success and edge cases"""
    payload = create_consult_payload(
        visit.pk, include_orders=False, include_diagnoses=False
    )
    # Successful case - create consult
    response = api_client.post(
        reverse("consults:consults_list"),
        payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201

    consult = Consult.objects.get(pk=1)
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - missing required doctor header
    response = api_client.post(
        reverse("consults:consults_list"),
        payload,
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
    missing_visit_dummy = payload.copy()
    missing_visit_dummy.get("consult", {}).pop("visit_id", None)
    response = api_client.post(
        reverse("consults:consults_list"),
        missing_visit_dummy,
        headers={"doctor": test_user.email},
    )

    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")
    assert response.data["error"].find("visit_id") != -1

    # Edge case - invalid visit_id
    invalid_visit_dummy = payload.copy()
    invalid_visit_dummy.get("consult", {}).update({"visit_id": "invalid_id"})
    response = api_client.post(
        reverse("consults:consults_list"),
        invalid_visit_dummy,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Invalid")
    assert response.data["error"].find("visit_id") != -1

    # Edge case - nonexistent visit_id
    nonexistent_visit_dummy = payload.copy()
    nonexistent_visit_dummy.get("consult", {}).update({"visit_id": 99999})
    response = api_client.post(
        reverse("consults:consults_list"),
        nonexistent_visit_dummy,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Cannot find")
    assert response.data["error"].find("visit_id") != -1


@pytest.mark.django_db
def test_consult_post_payload(api_client, visit, test_user, medications_many):
    """Test creating consults via POST - various payload edge cases"""
    base_payload = create_consult_payload(visit.pk)
    assert Diagnosis.objects.all().count() == 0, "Non-Empty Diagnosis Table"
    assert Order.objects.all().count() == 0, "Non-Empty Orders Table"

    # Edge case - missing diagnoses and orders (should still succeed)
    payload_no_diag_order = base_payload.copy()
    del payload_no_diag_order["diagnoses"]
    del payload_no_diag_order["orders"]
    response = api_client.post(
        reverse("consults:consults_list"),
        payload_no_diag_order,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    consult = Consult.objects.get(pk=response.data["id"])
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - empty diagnoses and orders lists
    payload_empty_diag_order = dict(base_payload)
    payload_empty_diag_order["diagnoses"] = []
    payload_empty_diag_order["orders"] = []
    response = api_client.post(
        reverse("consults:consults_list"),
        payload_empty_diag_order,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    consult = Consult.objects.get(pk=response.data["id"])
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Ensure that nothing is inserted into Diagnosis and Order tables
    assert Diagnosis.objects.all().count() == 0, "Non-Empty Diagnosis Table"
    assert Order.objects.all().count() == 0, "Non-Empty Orders Table"

    # Successful case - with diagnoses and orders
    response = api_client.post(
        reverse("consults:consults_list"),
        base_payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    consult_id = response.data["id"]
    consult = Consult.objects.get(pk=consult_id)
    expected_consult = ConsultSerializer(consult).data
    order = Order.objects.filter(consult_id=consult_id)
    diagnosis = Diagnosis.objects.filter(consult_id=consult_id)

    # TODO: replace the simple length check with more detailed one.
    assert (
        response.data == expected_consult
        and len(order) == len(base_payload.get("orders", []))
        and len(diagnosis) == len(base_payload.get("diagnoses", []))
    ), "Consult Mismatch with diagnoses and orders"

    # Edge case - invalid order data (should fail entire consult creation)
    num_consults_before = Consult.objects.all().count()
    invalid_order_payload = create_consult_payload(visit.pk)
    invalid_order_payload["orders"][0]["quantity"] = "invalid_quantity"
    response = api_client.post(
        reverse("consults:consults_list"),
        invalid_order_payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Invalid")
    assert response.data["error"].find("quantity") != -1
    assert Consult.objects.all().count() == num_consults_before

    # Edge case - invalid diagnosis data (should fail entire consult creation)
    num_consults_before = Consult.objects.all().count()
    invalid_diagnosis_payload = create_consult_payload(visit.pk)
    del invalid_diagnosis_payload["diagnoses"][0]["category"]
    response = api_client.post(
        reverse("consults:consults_list"),
        invalid_diagnosis_payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 400
    assert response.data["error"].startswith("Missing")
    assert response.data["error"].find("category") != -1
    assert Consult.objects.all().count() == num_consults_before


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
    assert response.status_code == 404
    assert response.data.get("error") == "Consult not found"


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
    assert response.status_code == 404
    assert response.data.get("error") == "Consult not found"


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
    assert response.status_code == 404
    assert response.data.get("error") == "Consult not found"

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
