"""
Pytest-style version of test_vitals.py
"""
import pytest
from rest_framework.reverse import reverse

from api.models import Vitals
from api.serializers import VitalsSerializer
import api.tests.dummies as dummy


@pytest.fixture
def patient_and_visit(api_client):
    """Create patient and visit via API calls (as in original setUp)"""
    patient_response = api_client.post(reverse("patients:patients_list"), dummy.post_patient_dummy)
    assert patient_response.status_code == 200

    visit_response = api_client.post(reverse("visits:visits_list"), dummy.post_visit_dummy)
    assert visit_response.status_code == 200

    return patient_response, visit_response


@pytest.mark.django_db
def test_vitals_api_crud_operations(api_client, patient_and_visit):
    """Test full CRUD lifecycle for vitals endpoint"""
    list_endpoint = "vitals:vitals_list"
    detail_endpoint = "vitals:vitals_pk"
    
    # POST - Create vitals
    post_response = api_client.post(reverse(list_endpoint), dummy.post_vitals_dummy)
    assert post_response.status_code == 200
    expected = VitalsSerializer(Vitals.objects.get(pk=1)).data
    assert post_response.data == expected

    # GET - Retrieve vitals
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected

    # PATCH - Update vitals
    put_response = api_client.patch(reverse(detail_endpoint, args=["1"]), dummy.post_vitals_dummy)
    assert put_response.status_code == 200
    assert put_response.data == expected

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected

    # DELETE - Remove vitals
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 200
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list by visit - Verify deletion (view requires either 'visit' or 'patientID' query param)
    get_response = api_client.get(reverse(list_endpoint) + "?visit=1")
    assert get_response.status_code == 200
    assert get_response.data == []
