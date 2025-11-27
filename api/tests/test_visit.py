"""
Pytest-style version of test_visit.py
"""
import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient
import api.tests.dummy as dummy


@pytest.fixture
def patient(db):
    """Create a test patient directly via ORM"""
    return Patient.objects.create(
        village_prefix=dummy.post_patient_dummy["village_prefix"],
        name=dummy.post_patient_dummy["name"],
        identification_number=dummy.post_patient_dummy.get("identification_number"),
        contact_no=dummy.post_patient_dummy.get("contact_no"),
        gender=dummy.post_patient_dummy.get("gender"),
        date_of_birth=timezone.make_aware(datetime(2021, 1, 1)),
        drug_allergy=dummy.post_patient_dummy.get("drug_allergy", "drug_allergy"),
        picture="image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
    )


@pytest.mark.django_db
def test_visit_api_crud_operations(api_client, patient):
    """Test full CRUD lifecycle for visit endpoint"""
    list_endpoint = "visits:visits_list"
    detail_endpoint = "visits:visits_pk"
    
    dummy_result = {
        "id": 1,
        "patient": {
            "model": "clinicmodels.patient",
            "pk": 1,
            "village_prefix": "VPF",
            "name": "patient_name",
            "identification_number": "identification_number",
            "contact_no": "contact_no",
            "gender": "gender",
            "date_of_birth": "2021-01-01T00:00:00Z",
            "drug_allergy": "drug_allergy",
            "face_encodings": None,
            "picture": "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
            "filter_string": "VPF001VPF1 contact_no patient_name",
            "patient_id": "VPF001",
        },
        "date": "2021-01-01T00:00:00Z",
        "status": "status",
    }
    
    # POST - Create visit
    post_response = api_client.post(reverse(list_endpoint), dummy.post_visit_dummy)
    assert post_response.status_code == 200
    
    # Check main visit fields and key patient attributes
    assert post_response.data.get("id") == 1
    assert post_response.data.get("date") == "2021-01-01T00:00:00Z"
    assert post_response.data.get("status") == "status"
    patient_data = post_response.data.get("patient")
    assert isinstance(patient_data, dict)
    for k in ("pk", "village_prefix", "name", "patient_id"):
        if k == "patient_id":
            expected_pid = f"{patient_data.get('village_prefix')}{int(patient_data.get('pk')):04d}"
            assert patient_data.get("patient_id") == expected_pid
        else:
            assert patient_data.get(k) == dummy_result["patient"].get(k)

    # GET - Retrieve visit
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    for k in ("id", "date", "status"):
        assert get_response.data.get(k) == post_response.data.get(k)
    patient_data = get_response.data.get("patient")
    for k in ("pk", "village_prefix", "name", "patient_id"):
        if k == "patient_id":
            expected_pid = f"{patient_data.get('village_prefix')}{int(patient_data.get('pk')):04d}"
            assert patient_data.get("patient_id") == expected_pid
        else:
            assert patient_data.get(k) == dummy_result["patient"].get(k)

    # PATCH - Update visit
    put_response = api_client.patch(reverse(detail_endpoint, args=["1"]), dummy.post_visit_dummy)
    assert put_response.status_code == 200
    for k in ("id", "date", "status"):
        assert put_response.data.get(k) == dummy_result.get(k)
    patient_data = put_response.data.get("patient")
    for k in ("pk", "village_prefix", "name", "patient_id"):
        if k == "patient_id":
            expected_pid = f"{patient_data.get('village_prefix')}{int(patient_data.get('pk')):04d}"
            assert patient_data.get("patient_id") == expected_pid
        else:
            assert patient_data.get(k) == dummy_result["patient"].get(k)

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    for k in ("id", "date", "status"):
        assert get_response.data.get(k) == dummy_result.get(k)
    patient_data = get_response.data.get("patient")
    for k in ("pk", "village_prefix", "name", "patient_id"):
        if k == "patient_id":
            expected_pid = f"{patient_data.get('village_prefix')}{int(patient_data.get('pk')):04d}"
            assert patient_data.get("patient_id") == expected_pid
        else:
            assert patient_data.get(k) == dummy_result["patient"].get(k)

    # DELETE - Remove visit
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 200
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list - Verify deletion
    get_response = api_client.get(reverse(list_endpoint))
    assert get_response.status_code == 200
    assert get_response.data == []
