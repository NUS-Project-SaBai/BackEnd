"""
GET tests for medications
"""

import pytest
from rest_framework.reverse import reverse

from api.serializers import MedicationSerializer
from api.models import Medication


@pytest.mark.django_db
def test_medications_get_SingleAndList(api_client, medication_instance):
    """Test retrieving medications via GET - single, list, and edge cases"""
    payload = {}
    # Successful case - retrieve single medication by pk
    response = api_client.get(
        reverse("medication:medications_pk", args=[str(medication_instance)])
    )
    assert response.status_code == 200

    # Successful case - list medications
    response = api_client.get(reverse("medication:medications_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
