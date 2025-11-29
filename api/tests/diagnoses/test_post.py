"""
POST tests for diagnoses
"""

import pytest
from rest_framework.reverse import reverse

from api.tests.factories import diagnosis_payloads
from api.models import Diagnosis
from api.serializers import DiagnosisSerializer


@pytest.mark.django_db
def test_diagnoses_post_SuccessCreate(api_client, consult):
    """Test creating diagnoses via POST - success and edge cases"""
    # Successful case - create diagnosis
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.post(reverse("diagnosis:diagnosis_list"), diagnosis_data)
    assert response.status_code == 201
    expected = DiagnosisSerializer(Diagnosis.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty diagnosis data
    response = api_client.post(reverse("diagnosis:diagnosis_list"), {})
    assert response.status_code == 400
