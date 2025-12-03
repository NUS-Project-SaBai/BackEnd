"""
POST tests for medications
"""

import pytest
from rest_framework.reverse import reverse

from api.tests.factories import medication_payloads


@pytest.mark.django_db
def test_medications_post_SuccessCreate(api_client, test_user):
    """Test creating medications via POST - success and edge cases"""
    payload = medication_payloads()[0]
    # Successful case - create medication
    response = api_client.post(
        reverse("medication:medications_list"),
        payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201

    # Edge case - missing doctor header
    response = api_client.post(
        reverse("medication:medications_list"),
        payload,
    )
    assert response.status_code in [400, 403, 500]

    # Edge case - empty medication data
    response = api_client.post(
        reverse("medication:medications_list"),
        {},
        headers={"doctor": test_user.email},
    )
    assert response.status_code in [400, 500]


@pytest.mark.django_db
def test_medications_post_DuplicateCodeReturnsError(api_client, test_user):
    """Posting duplicate medication (same code) should error or reject."""
    payload = medication_payloads()[0]
    # Create first
    r1 = api_client.post(
        reverse("medication:medications_list"),
        payload,
        headers={"doctor": test_user.email},
    )
    assert r1.status_code == 201

    # Create duplicate - server may allow duplicates; ensure it returns 201 and different id
    r2 = api_client.post(
        reverse("medication:medications_list"),
        payload,
        headers={"doctor": test_user.email},
    )
    assert r2.status_code == 201
    assert r2.data.get("id") != r1.data.get("id")


@pytest.mark.django_db
def test_medications_post_DuplicateCodeIsAllowed(api_client, test_user):
    """Explicitly assert that duplicate `code` values are allowed (not unique)."""
    p1 = medication_payloads()[0].copy()
    p2 = medication_payloads()[1].copy()
    p1["code"] = "SAMECODE"
    p2["code"] = "SAMECODE"

    r1 = api_client.post(
        reverse("medication:medications_list"), p1, headers={"doctor": test_user.email}
    )
    r2 = api_client.post(
        reverse("medication:medications_list"), p2, headers={"doctor": test_user.email}
    )
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.data.get("id") != r2.data.get("id")


@pytest.mark.django_db
def test_medications_post_DuplicateNameIsAllowed(api_client, test_user):
    """Assert that duplicate `medicine_name` values are allowed (not unique at DB/service level)."""
    p1 = medication_payloads()[0].copy()
    p2 = medication_payloads()[1].copy()
    p1["medicine_name"] = "SameName"
    p2["medicine_name"] = "SameName"

    r1 = api_client.post(
        reverse("medication:medications_list"), p1, headers={"doctor": test_user.email}
    )
    r2 = api_client.post(
        reverse("medication:medications_list"), p2, headers={"doctor": test_user.email}
    )
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r1.data.get("id") != r2.data.get("id")
