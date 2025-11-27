"""
Pytest-style version of test_orders.py
"""
import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient, Visit, Order
from api.serializers import OrderSerializer
import api.tests.dummy as dummy


@pytest.fixture
def patient(db):
    """Create a test patient"""
    return Patient.objects.create(
        village_prefix=dummy.post_patient_dummy.get("village_prefix", "VPF"),
        name=dummy.post_patient_dummy.get("name", "patient_name"),
        identification_number=dummy.post_patient_dummy.get("identification_number"),
        contact_no=dummy.post_patient_dummy.get("contact_no"),
        gender=dummy.post_patient_dummy.get("gender", "gender"),
        date_of_birth=timezone.make_aware(
            datetime.fromisoformat(dummy.post_patient_dummy.get("date_of_birth"))
        ),
        drug_allergy=dummy.post_patient_dummy.get("drug_allergy", "drug_allergy"),
        face_encodings=dummy.post_patient_dummy.get("face_encodings", ""),
        picture=dummy.post_patient_dummy.get("picture", "image/upload/v1/dummy.jpg"),
    )


@pytest.fixture
def visit(patient):
    """Create a test visit"""
    return Visit.objects.create(
        patient=patient,
        date=timezone.make_aware(
            datetime.fromisoformat(dummy.post_visit_dummy.get("date"))
        ),
        status=dummy.post_visit_dummy.get("status"),
    )


@pytest.fixture
def consult_and_medication(api_client, visit, test_user):
    """Create consult and medication via API calls (as in original setUp)"""
    # Create consult under expected wrapper and include doctor header
    consult_response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
        HTTP_DOCTOR=test_user.email
    )
    assert consult_response.status_code == 201
    
    # Create medication with doctor header
    medication_response = api_client.post(
        reverse("medication:medications_list"),
        dummy.post_medication_dummy,
        HTTP_DOCTOR=test_user.email
    )
    assert medication_response.status_code == 201
    
    return consult_response, medication_response


@pytest.mark.django_db
def test_orders_api_crud_operations(api_client, consult_and_medication):
    """Test full CRUD lifecycle for orders endpoint"""
    list_endpoint = "orders:orders_list"
    detail_endpoint = "orders:orders_pk"
    
    # POST - Create order
    post_response = api_client.post(reverse(list_endpoint), dummy.post_order_dummy)
    assert post_response.status_code == 201
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert post_response.data == expected

    # GET - Retrieve order
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert get_response.data == expected

    # PATCH - Update order status
    put_response = api_client.patch(
        reverse(detail_endpoint, args=["1"]), 
        {"order_status": "PENDING"}
    )
    assert put_response.status_code == 200
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert put_response.data == expected

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    expected = OrderSerializer(Order.objects.get(pk=1)).data
    assert get_response.data == expected

    # DELETE - Remove order
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 200
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list - Verify deletion
    get_response = api_client.get(reverse(list_endpoint))
    assert get_response.status_code == 200
    assert get_response.data == []
