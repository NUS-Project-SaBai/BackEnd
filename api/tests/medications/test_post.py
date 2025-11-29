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
