"""
DELETE tests for vitals
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_vitals_delete_RemovesAndEdgeCases(api_client, vitals_instance):
    """Test deleting vitals via DELETE - success and edge cases"""
    vitals_pk = vitals_instance.pk
    visit_pk = vitals_instance.visit.pk

    # Successful case - delete vitals
    response = api_client.delete(reverse("vitals:vitals_pk", args=[str(vitals_pk)]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify vitals is gone from list
    response = api_client.get(reverse("vitals:vitals_list") + f"?visit={visit_pk}")
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted vitals (should 404)
    response = api_client.delete(reverse("vitals:vitals_pk", args=[str(vitals_pk)]))
    assert response.status_code == 404

    # Edge case - delete nonexistent vitals
    response = api_client.delete(reverse("vitals:vitals_pk", args=["99999"]))
    assert response.status_code == 404
