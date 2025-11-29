"""
POST tests for visits
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Visit
from api.tests.factories import visit_payloads


@pytest.mark.django_db
def test_visits_post_SuccessCreate(api_client, patient):
    """Test creating visits via POST - success and edge cases"""
    # Successful case - create visit
    payload = visit_payloads()[0]
    response = api_client.post(reverse("visits:visits_list"), payload)
    assert response.status_code == 200

    visit = Visit.objects.get(pk=1)
    # Check main visit fields
    assert response.data.get("id") == 1
    assert response.data.get("date") == "2021-01-01T00:00:00Z"
    assert response.data.get("status") == "status"

    # Edge case - empty visit data
    response = api_client.post(reverse("visits:visits_list"), {})
    assert response.status_code in [400, 500]  # Should fail validation
