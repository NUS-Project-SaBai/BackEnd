"""
DELETE tests for consults
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_consults_delete_RemovesAndEdgeCases(api_client, consult):
    """Test deleting consults via DELETE - success and edge cases"""
    visit_id = consult.visit.pk
    consult_id = consult.pk

    # Successful case - delete consult
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_id)])
    )
    assert response.status_code == 204
    assert response.data == {"message": "Deleted successfully"}

    # Verify consult is gone from list
    response = api_client.get(
        reverse("consults:consults_list") + f"?visit_id={visit_id}"
    )
    assert response.status_code == 200
    assert response.data == []

    response = api_client.get(reverse("consults:consults_pk", args=[str(consult_id)]))
    assert response.status_code == 404
    assert response.data.get("error") == "Consult not found"

    # Edge case - delete already deleted consult (should 404)
    response = api_client.delete(
        reverse("consults:consults_pk", args=[str(consult_id)])
    )
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )

    # Edge case - delete nonexistent consult
    response = api_client.delete(reverse("consults:consults_pk", args=["99999"]))
    assert (
        response.status_code == 404
        and response.data.get("error") == "Consult not found"
    )
