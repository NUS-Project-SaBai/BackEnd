"""
Test visit API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Visit
import api.tests.dummies as dummy
from api.tests.factories import visit_payloads


@pytest.fixture
def visit_instance(api_client, patient):
    """Create a visit instance for tests that need existing data"""
    payload = visit_payloads()[0]
    response = api_client.post(reverse("visits:visits_list"), payload)
    assert response.status_code == 200
    return Visit.objects.get(pk=response.data["id"])


@pytest.mark.django_db
def test_visit_post(api_client, patient):
    """Test creating visits via POST - success and edge cases"""
    # Successful case - create visit
    payload = visit_payloads()[0]
    response = api_client.post(reverse("visits:visits_list"), payload)
    assert response.status_code == 200

    visit = Visit.objects.get(pk=1)
    # Check main visit fields
    assert response.data.get("id") == 1
    assert response.data.get("date") == "2021-01-01T00:00:00Z"
    assert response.data.get("status") == "status"

    # Edge case - empty visit data
    response = api_client.post(reverse("visits:visits_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation


@pytest.mark.django_db
def test_visit_get(api_client, visit_instance):
    """Test retrieving visits via GET - single, list, and edge cases"""
    # Successful case - retrieve single visit by pk
    response = api_client.get(
        reverse("visits:visits_pk", args=[str(visit_instance.pk)])
    )
    assert response.status_code == 200
    assert response.data.get("id") == visit_instance.pk
    assert response.data.get("date") == "2021-01-01T00:00:00Z"
    assert response.data.get("status") == "status"

    # Successful case - list visits
    response = api_client.get(reverse("visits:visits_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == visit_instance.pk

    # Edge case - get nonexistent visit
    response = api_client.get(reverse("visits:visits_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_visit_patch(api_client, visit_instance):
    """Test updating visits via PATCH - success and edge cases"""
    # Successful case - update visit
    payload = visit_payloads()[0]
    response = api_client.patch(
        reverse("visits:visits_pk", args=[str(visit_instance.pk)]),
        payload,
    )
    assert response.status_code == 200
    assert response.data.get("id") == visit_instance.pk
    assert response.data.get("date") == "2021-01-01T00:00:00Z"
    assert response.data.get("status") == "status"

    # Edge case - update nonexistent visit
    response = api_client.patch(reverse("visits:visits_pk", args=["99999"]), payload)
    assert response.status_code == 404


@pytest.mark.django_db
def test_visit_delete(api_client, visit_instance):
    """Test deleting visits via DELETE - success and edge cases"""
    visit_pk = visit_instance.pk

    # Successful case - delete visit
    response = api_client.delete(reverse("visits:visits_pk", args=[str(visit_pk)]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify visit is gone from list
    response = api_client.get(reverse("visits:visits_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted visit (should 404)
    response = api_client.delete(reverse("visits:visits_pk", args=[str(visit_pk)]))
    assert response.status_code == 404

    # Edge case - delete nonexistent visit
    response = api_client.delete(reverse("visits:visits_pk", args=["99999"]))
    assert response.status_code == 404
