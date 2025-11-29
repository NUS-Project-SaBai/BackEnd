import pytest
from rest_framework.reverse import reverse

from api.models import Vitals
from api.tests.factories import vitals_payloads


@pytest.fixture
def vitals_instance(api_client, patient_and_visit):
    """Create a vitals instance for tests that need existing data"""
    payload = vitals_payloads()[0]
    response = api_client.post(reverse("vitals:vitals_list"), payload)
    assert response.status_code == 200
    return Vitals.objects.get(pk=response.data["id"])
