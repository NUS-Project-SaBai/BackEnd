import pytest
from rest_framework.reverse import reverse

from api.models import Visit
from api.tests.factories import visit_payloads


@pytest.fixture
def visit_instance(api_client, patient):
    """Create a visit instance for tests that need existing data"""
    payload = visit_payloads()[0]
    response = api_client.post(reverse("visits:visits_list"), payload)
    assert response.status_code == 200
    return Visit.objects.get(pk=response.data["id"])
