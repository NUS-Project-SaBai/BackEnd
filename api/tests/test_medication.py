"""
Pytest-style version of test_medication.py
"""
import pytest
from rest_framework.reverse import reverse

import api.tests.dummies as dummy


@pytest.mark.django_db
def test_medication_api_crud_operations(api_client, test_user):
    """Test full CRUD lifecycle for medication endpoint"""
    list_endpoint = "medication:medications_list"
    detail_endpoint = "medication:medications_pk"
    
    # POST - Create medication with doctor header
    post_response = api_client.post(
        reverse(list_endpoint),
        dummy.post_medication_dummy,
        HTTP_DOCTOR=test_user.email,
    )
    assert post_response.status_code == 201
    
    # Medication serializer returns medication fields; approval is write-only
    expected_post = {
        "id": 1,
        "medicine_name": dummy.post_medication_dummy["medicine_name"],
        "quantity": dummy.post_medication_dummy["quantity"],
        "notes": dummy.post_medication_dummy["notes"],
        "code": None,
        "warning_quantity": None,
    }
    assert post_response.data == expected_post

    # GET - Retrieve medication
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected_post

    # PATCH - Update medication with doctor header
    put_response = api_client.patch(
        reverse(detail_endpoint, args=["1"]),
        dummy.post_medication_dummy,
        HTTP_DOCTOR=test_user.email,
    )
    assert put_response.status_code == 200
    assert put_response.data == expected_post

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected_post

    # DELETE - Remove medication
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 200
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list - Verify deletion
    get_response = api_client.get(reverse(list_endpoint))
    assert get_response.status_code == 200
    assert get_response.data == []
