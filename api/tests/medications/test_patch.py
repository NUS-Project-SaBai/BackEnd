"""
PATCH tests for medications
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_medications_patch_SuccessUpdate(api_client, medication_instance, test_user):
    """PATCH with an empty payload should be a no-op and preserve resource state.

    Also assert that updating a non-existent resource returns 404.
    """
    # Fetch current state
    before = api_client.get(
        reverse("medication:medications_pk", args=[str(medication_instance)])
    )
    assert before.status_code == 200

    # No-op patch (empty payload) should succeed and not change stored values
    response = api_client.patch(
        reverse("medication:medications_pk", args=[str(medication_instance)]),
        {},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 200

    after = api_client.get(
        reverse("medication:medications_pk", args=[str(medication_instance)])
    )
    assert after.status_code == 200
    assert after.data == before.data

    # Edge case - update nonexistent medication returns 404
    response = api_client.patch(
        reverse("medication:medications_pk", args=["99999"]),
        {},
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_medications_patch_UpdateFieldsPersists(
    api_client, medication_instance, test_user
):
    """Ensure updating name/code changes the stored resource."""
    new_data = {"medicine_name": "Updated Medicine Name", "code": "UPD-CODE-123"}
    r = api_client.patch(
        reverse("medication:medications_pk", args=[str(medication_instance)]),
        new_data,
        headers={"doctor": test_user.email},
    )
    assert r.status_code == 200

    # Fetch and confirm
    get_r = api_client.get(
        reverse("medication:medications_pk", args=[str(medication_instance)])
    )
    assert get_r.status_code == 200
    assert get_r.data.get("medicine_name") == new_data["medicine_name"]
    assert get_r.data.get("code") == new_data["code"]
