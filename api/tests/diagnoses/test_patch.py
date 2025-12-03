"""
PATCH tests for diagnoses
"""

import pytest
from rest_framework.reverse import reverse

from api.tests.factories import diagnosis_payloads
from api.serializers import DiagnosisSerializer


@pytest.mark.django_db
def test_diagnoses_patch_SuccessUpdate(api_client, diagnosis_instance, consult):
    """Test updating diagnoses via PATCH - success and edge cases"""
    # Successful case - update diagnosis
    payload = diagnosis_payloads()[0]
    diagnosis_data = {
        "consult_id": consult.pk,
        "details": payload.get("details"),
        "category": payload.get("category"),
    }
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_instance.pk)]),
        diagnosis_data,
    )
    assert response.status_code == 200
    expected = DiagnosisSerializer(diagnosis_instance).data
    assert response.data == expected

    # Edge case - update nonexistent diagnosis - fail
    response = api_client.patch(
        reverse("diagnosis:diagnosis_pk", args=["99999"]), diagnosis_data
    )
    assert response.status_code == 404
