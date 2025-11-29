import pytest
from rest_framework.reverse import reverse

from api.tests.factories import medication_payloads


@pytest.fixture
def medication_instance(api_client, test_user):
    """Create a medication instance for tests that need existing data"""
    payload = medication_payloads()[0]
    response = api_client.post(
        reverse("medication:medications_list"),
        payload,
        headers={"doctor": test_user.email},
    )
    assert response.status_code == 201
    return response.data["id"]
