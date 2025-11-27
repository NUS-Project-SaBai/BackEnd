"""
Test vitals API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Vitals
from api.serializers import VitalsSerializer
import api.tests.dummies as dummy


@pytest.fixture
def vitals_instance(api_client, patient_and_visit):
    """Create a vitals instance for tests that need existing data"""
    response = api_client.post(reverse("vitals:vitals_list"), dummy.post_vitals_dummy)
    assert response.status_code == 200
    return Vitals.objects.get(pk=response.data["id"])


@pytest.mark.django_db
def test_vitals_post(api_client, patient_and_visit):
    """Test creating vitals via POST - success and edge cases"""
    # Successful case - create vitals
    response = api_client.post(reverse("vitals:vitals_list"), dummy.post_vitals_dummy)
    assert response.status_code == 200
    expected = VitalsSerializer(Vitals.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty vitals data
    response = api_client.post(reverse("vitals:vitals_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation


@pytest.mark.django_db
def test_vitals_get(api_client, vitals_instance):
    """Test retrieving vitals via GET - single, list, and edge cases"""
    # Successful case - retrieve single vitals by pk
    response = api_client.get(
        reverse("vitals:vitals_pk", args=[str(vitals_instance.pk)])
    )
    assert response.status_code == 200
    expected = VitalsSerializer(vitals_instance).data
    assert response.data == expected

    # Successful case - list vitals by visit
    response = api_client.get(
        reverse("vitals:vitals_list") + f"?visit={vitals_instance.visit.pk}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == vitals_instance.pk

    # Edge case - get nonexistent vitals
    response = api_client.get(reverse("vitals:vitals_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_vitals_patch(api_client, vitals_instance):
    """Test updating vitals via PATCH - success and edge cases"""
    # Successful case - update vitals
    response = api_client.patch(
        reverse("vitals:vitals_pk", args=[str(vitals_instance.pk)]),
        dummy.post_vitals_dummy,
    )
    assert response.status_code == 200
    expected = VitalsSerializer(vitals_instance).data
    assert response.data == expected

    # Edge case - update nonexistent vitals
    response = api_client.patch(
        reverse("vitals:vitals_pk", args=["99999"]), dummy.post_vitals_dummy
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_vitals_delete(api_client, vitals_instance):
    """Test deleting vitals via DELETE - success and edge cases"""
    vitals_pk = vitals_instance.pk
    visit_pk = vitals_instance.visit.pk

    # Successful case - delete vitals
    response = api_client.delete(reverse("vitals:vitals_pk", args=[str(vitals_pk)]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify vitals is gone from list
    response = api_client.get(reverse("vitals:vitals_list") + f"?visit={visit_pk}")
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted vitals (should 404)
    response = api_client.delete(reverse("vitals:vitals_pk", args=[str(vitals_pk)]))
    assert response.status_code == 404

    # Edge case - delete nonexistent vitals
    response = api_client.delete(reverse("vitals:vitals_pk", args=["99999"]))
    assert response.status_code == 404
