import pytest
from rest_framework.reverse import reverse

from api.models import Diagnosis
from api.tests.factories import diagnosis_payloads


@pytest.fixture
def diagnosis_instance(api_client, consult):
    """Create a diagnosis instance for tests that need existing data"""
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.post(reverse("diagnosis:diagnosis_list"), diagnosis_data)
    assert response.status_code == 201
    return Diagnosis.objects.get(pk=response.data["id"])
