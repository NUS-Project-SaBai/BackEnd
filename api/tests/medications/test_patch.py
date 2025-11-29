"""
PATCH tests for medications
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_medications_patch_SuccessUpdate(api_client, medication_instance, test_user):
    """Test updating medications via PATCH - success and edge cases"""
    payload = {}
    # Successful case - update medication
    response = api_client.patch(
        reverse("medication:medications_pk", args=[str(medication_instance)]),
        payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 200

    # Edge case - update nonexistent medication
    response = api_client.patch(
        reverse("medication:medications_pk", args=["99999"]),
        payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 404
