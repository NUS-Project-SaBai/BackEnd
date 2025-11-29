"""
POST tests for vitals
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Vitals
from api.serializers import VitalsSerializer
from api.tests.factories import vitals_payloads


@pytest.mark.django_db
def test_vitals_post_SuccessCreate(api_client, patient_and_visit):
    """Test creating vitals via POST - success and edge cases"""
    # Successful case - create vitals
    payload = vitals_payloads()[0]
    response = api_client.post(reverse("vitals:vitals_list"), payload)
    assert response.status_code == 200
    expected = VitalsSerializer(Vitals.objects.get(pk=1)).data
    assert response.data == expected

    # Edge case - empty vitals data
    response = api_client.post(reverse("vitals:vitals_list"), {})
    assert response.status_code in [400, 500]
