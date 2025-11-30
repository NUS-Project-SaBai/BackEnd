"""
GET tests for medications
"""

import pytest
from rest_framework.reverse import reverse

from api.serializers import MedicationSerializer
from api.models import Medication
from api.tests.factories import medication_payloads


@pytest.mark.django_db
def test_medications_get_SingleAndList(api_client, medication_instance):
    """Test retrieving medications via GET - single, list, and edge cases"""
    payload = {}
    # Successful case - retrieve single medication by pk
    response = api_client.get(
        reverse("medication:medications_pk", args=[str(medication_instance)])
    )
    assert response.status_code == 200

    # Successful case - list medications
    response = api_client.get(reverse("medication:medications_list"))
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_medications_get_NonexistentReturns404(api_client):
    """GETting a nonexistent medication may return 404 or 200 with empty body."""
    response = api_client.get(reverse("medication:medications_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_medications_get_FilterByName(api_client, test_user, medication_instance):
    """Create another medication and verify filtering by medicine_name."""
    second = medication_payloads()[1]
    r = api_client.post(
        reverse("medication:medications_list"),
        second,
        headers={"doctor": test_user.email},
    )
    assert r.status_code == 201

    # Filter by medicine_name substring
    name = second.get("medicine_name", "")
    resp_name = api_client.get(reverse("medication:medications_list") + f"?name={name}")
    assert resp_name.status_code == 200
    assert any(
        name.lower() in (m.get("medicine_name", "").lower()) for m in resp_name.data
    )


@pytest.mark.django_db
def test_medications_get_MultipleMatchesReturned(api_client, test_user):
    """Create multiple medications with same name and ensure filter returns both."""
    p1 = medication_payloads()[0].copy()
    p1["medicine_name"] = "dupmed"
    r1 = api_client.post(
        reverse("medication:medications_list"), p1, headers={"doctor": test_user.email}
    )
    assert r1.status_code == 201

    p2 = medication_payloads()[1].copy()
    p2["medicine_name"] = "dupmed"
    r2 = api_client.post(
        reverse("medication:medications_list"), p2, headers={"doctor": test_user.email}
    )
    assert r2.status_code == 201

    resp = api_client.get(reverse("medication:medications_list") + "?name=dupmed")
    assert resp.status_code == 200
    assert isinstance(resp.data, list)
    count = sum(1 for m in resp.data if m.get("medicine_name", "").lower() == "dupmed")
    assert count >= 2
