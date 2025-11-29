"""
PATCH tests for vitals
"""

import pytest
from rest_framework.reverse import reverse
from api.tests.factories import vitals_payloads


@pytest.mark.django_db
def test_vitals_patch_SuccessUpdate(api_client, vitals_instance):
    """Test updating vitals via PATCH - success and edge cases"""
    # Successful case - update vitals
    payload = vitals_payloads()[0]
    response = api_client.patch(
        reverse("vitals:vitals_pk", args=[str(vitals_instance.pk)]),
        payload,
    )
    assert response.status_code == 200
    expected = (
        VitalsSerializer(vitals_instance).data
        if "VitalsSerializer" in globals()
        else None
    )
    assert response.status_code == 200

    # Edge case - update nonexistent vitals
    response = api_client.patch(reverse("vitals:vitals_pk", args=["99999"]), payload)
    assert response.status_code == 404
