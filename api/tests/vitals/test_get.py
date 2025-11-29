"""
GET tests for vitals
"""

import pytest
from rest_framework.reverse import reverse

from api.serializers import VitalsSerializer


@pytest.mark.django_db
def test_vitals_get_SingleAndList(api_client, vitals_instance):
    """Test retrieving vitals via GET - single, list, and edge cases"""
    # Successful case - retrieve single vitals by pk
    response = api_client.get(
        reverse("vitals:vitals_pk", args=[str(vitals_instance.pk)])
    )
    assert response.status_code == 200
    expected = VitalsSerializer(vitals_instance).data
    assert response.data == expected

    # Successful case - list vitals by visit
    response = api_client.get(
        reverse("vitals:vitals_list") + f"?visit={vitals_instance.visit.pk}"
    )
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == vitals_instance.pk

    # Edge case - get nonexistent vitals
    response = api_client.get(reverse("vitals:vitals_pk", args=["99999"]))
    assert response.status_code == 404
