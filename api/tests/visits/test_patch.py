"""
PATCH tests for visits
"""

import pytest
from rest_framework.reverse import reverse

from api.tests.factories import visit_payloads


@pytest.mark.django_db
def test_visits_patch_SuccessUpdate(api_client, visit_instance):
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
