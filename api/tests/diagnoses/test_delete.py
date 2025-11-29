"""
DELETE tests for diagnoses
"""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_diagnoses_delete_RemovesAndEdgeCases(api_client, diagnosis_instance):
    """Test deleting diagnoses via DELETE - success and edge cases"""
    diagnosis_pk = diagnosis_instance.pk

    # Successful case - delete diagnosis
    response = api_client.delete(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_pk)])
    )
    assert response.status_code == 204
    assert response.data == {"message": "Deleted successfully"}

    # Verify diagnosis is gone from list
    response = api_client.get(reverse("diagnosis:diagnosis_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted diagnosis (should 404)
    response = api_client.delete(
        reverse("diagnosis:diagnosis_pk", args=[str(diagnosis_pk)])
    )
    assert response.status_code == 404

    # Edge case - delete nonexistent diagnosis
    response = api_client.delete(reverse("diagnosis:diagnosis_pk", args=["99999"]))
    assert response.status_code == 404
