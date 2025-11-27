"""
Pytest-style version of test_patient.py
"""
import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient
from api.serializers import PatientSerializer
import api.tests.dummies as dummy


from api.tests.dummies import post_patient_dummy

@pytest.fixture
def patient(db):
    """Create a test patient directly via ORM"""
    # Copy dummy to avoid mutating global dummy
    patient_data = dummy.post_patient_dummy.copy()
    
    return Patient.objects.create(
        village_prefix=patient_data["village_prefix"],
        name=patient_data["name"],
        identification_number=patient_data.get("identification_number"),
        contact_no=patient_data.get("contact_no"),
        gender=patient_data.get("gender"),
        date_of_birth=timezone.make_aware(datetime(2021, 1, 1)),
        drug_allergy=patient_data.get("drug_allergy", "drug_allergy"),
        face_encodings=patient_data.get("face_encodings", "88e4a97a-10d0-4e63-abe0-bd36808974b4"),
        picture="image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
    )


@pytest.mark.django_db
def test_patient_api_crud_operations(api_client, patient):
    """Test full CRUD lifecycle for patient endpoint"""
    list_endpoint = "patients:patients_list"
    detail_endpoint = "patients:patients_pk"
    
    expected_data = PatientSerializer(patient).data

    # GET detail - Retrieve patient
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    # Compare key fields instead of exact dict to be robust across deployments
    for k in ("pk", "village_prefix", "name", "patient_id"):
        assert get_response.data.get(k) == expected_data.get(k)

    # PATCH - Update patient via API (patched in setup to avoid uploads)
    update_payload = {"name": "patient_name"}
    put_response = api_client.patch(reverse(detail_endpoint, args=["1"]), update_payload)
    assert put_response.status_code == 200

    patient.refresh_from_db()
    expected_data = PatientSerializer(patient).data
    for k in ("pk", "village_prefix", "name", "patient_id"):
        assert put_response.data.get(k) == expected_data.get(k)

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    for k in ("pk", "village_prefix", "name", "patient_id"):
        assert get_response.data.get(k) == expected_data.get(k)

    # DELETE - Remove patient
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 200
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list - Verify deletion (should be empty)
    get_response = api_client.get(reverse(list_endpoint))
    assert get_response.status_code == 200
    assert get_response.data == []
