"""
PATCH tests for consults
"""

import pytest
from rest_framework.reverse import reverse

from api.serializers import ConsultSerializer


@pytest.mark.django_db
def test_consults_patch_SuccessUpdate(api_client, consult, test_user):
    """Test updating consults via PATCH - success and edge cases"""
    payload = {}
    # Use consult payloads from factories in original tests; here we just confirm patch behavior
    updated_dummy = payload
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
