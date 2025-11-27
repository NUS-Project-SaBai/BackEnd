"""
Test consult API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

import api.tests.dummies as dummy
from api.models import Consult
from api.serializers import ConsultSerializer


@pytest.fixture
def consult_instance(api_client, visit, test_user):
    """Create a consult instance for tests that need existing data"""
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    return Consult.objects.get(pk=response.data["id"])


@pytest.mark.django_db
def test_consult_post(api_client, visit, test_user):
    """Test creating consults via POST - success and edge cases"""
    # Successful case - create consult
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201

    consult = Consult.objects.get(pk=1)
    expected = ConsultSerializer(consult).data
    assert response.data == expected

    # Edge case - missing required doctor header
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
    )
    assert response.status_code in [400, 403, 500]  # Should fail without doctor

    # Edge case - empty consult data
    response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": {}},
        headers={"doctor": test_user.email},
    )
    assert response.status_code in [400, 500]  # Should fail validation


@pytest.mark.django_db
def test_consult_get(api_client, consult_instance):
    """Test retrieving consults via GET - single, list, and edge cases"""
    # Successful case - retrieve single consult by pk
    response = api_client.get(
        reverse("consults:consults_pk", args=[str(consult_instance.pk)])
    )
    assert response.status_code == 200
    expected = ConsultSerializer(consult_instance).data
    assert response.data == expected

    # Successful case - list consults by visit
    response = api_client.get(
        reverse("consults:consults_list") + f"?visit={consult_instance.visit.pk}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == consult_instance.pk

    # Edge case - get nonexistent consult
    response = api_client.get(reverse("consults:consults_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_consult_patch(api_client, consult_instance, test_user):
    """Test updating consults via PATCH - success and edge cases"""
    # Successful case - update consult
    updated_dummy = dummy.post_consult_dummy.copy()
    response = api_client.patch(
        reverse("consults:consults_pk", args=[str(consult_instance.pk)]),
        {"consult": updated_dummy},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 200

    consult_instance.refresh_from_db()
    expected = ConsultSerializer(consult_instance).data
    assert response.data == expected

    # Edge case - update nonexistent consult
    response = api_client.patch(
        reverse("consults:consults_pk", args=["99999"]),
        {"consult": updated_dummy},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_consult_delete(api_client, consult_instance):
    """Test deleting consults via DELETE - success and edge cases"""
    visit_pk = consult_instance.visit.pk
    consult_pk = consult_instance.pk

    # Successful case - delete consult
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_pk)])
    )
    assert response.status_code == 204
    assert response.data == {"message": "Deleted successfully"}

    # Verify consult is gone from list
    response = api_client.get(reverse("consults:consults_list") + f"?visit={visit_pk}")
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted consult (should 404)
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_pk)])
    )
    assert response.status_code == 404

    # Edge case - delete nonexistent consult
    response = api_client.delete(reverse("consults:consults_pk", args=["99999"]))
    assert response.status_code == 404
