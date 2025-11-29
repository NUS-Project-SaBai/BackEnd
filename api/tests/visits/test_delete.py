"""
DELETE tests for visits
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_visits_delete_RemovesAndEdgeCases(api_client, visit_instance):
    """Test deleting visits via DELETE - success and edge cases"""
    visit_pk = visit_instance.pk

    # Successful case - delete visit
    response = api_client.delete(reverse("visits:visits_pk", args=[str(visit_pk)]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify visit is gone from list
    response = api_client.get(reverse("visits:visits_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted visit (should 404)
    response = api_client.delete(reverse("visits:visits_pk", args=[str(visit_pk)]))
    assert response.status_code == 404

    # Edge case - delete nonexistent visit
    response = api_client.delete(reverse("visits:visits_pk", args=["99999"]))
    assert response.status_code == 404
