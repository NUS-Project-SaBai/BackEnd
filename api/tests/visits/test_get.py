"""
GET tests for visits
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Visit


@pytest.mark.django_db
def test_visits_get_SingleAndList(api_client, visit_instance):
    """Test retrieving visits via GET - single, list, and edge cases"""
    # Successful case - retrieve single visit by pk
    response = api_client.get(
        reverse("visits:visits_pk", args=[str(visit_instance.pk)])
    )
    assert response.status_code == 200
    assert response.data.get("id") == visit_instance.pk
    assert response.data.get("date") == "2021-01-01T00:00:00Z"
    assert response.data.get("status") == "status"

    # Successful case - list visits
    response = api_client.get(reverse("visits:visits_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == visit_instance.pk

    # Edge case - get nonexistent visit
    response = api_client.get(reverse("visits:visits_pk", args=["99999"]))
    assert response.status_code == 404
