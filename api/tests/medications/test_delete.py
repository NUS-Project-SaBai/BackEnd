"""
DELETE tests for medications
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_medications_delete_RemovesAndEdgeCases(api_client, medication_instance):
    """Test deleting medications via DELETE - success and edge cases"""
    medication_pk = medication_instance

    # Successful case - delete medication
    response = api_client.delete(
        reverse("medication:medications_pk", args=[str(medication_pk)])
    )
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify medication is gone from list
    response = api_client.get(reverse("medication:medications_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted medication (returns 500)
    response = api_client.delete(
        reverse("medication:medications_pk", args=[str(medication_pk)])
    )
    assert response.status_code == 404

    # Edge case - delete nonexistent medication
    response = api_client.delete(reverse("medication:medications_pk", args=["99999"]))
    assert response.status_code == 404
