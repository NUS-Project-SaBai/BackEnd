"""DELETE tests for patients resource."""

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_patients_delete_RemovesAndSubsequent404(api_client, patient_instance):
    """DELETE should remove the patient and subsequent deletes return 404"""
    patient_pk = patient_instance.pk
    response = api_client.delete(reverse("patients:patients_pk", args=[patient_pk]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify gone
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert response.data == []

    # Deleting again returns 404
    response = api_client.delete(
        reverse("patients:patients_pk", args=[str(patient_pk)])
    )
    assert response.status_code == 404
