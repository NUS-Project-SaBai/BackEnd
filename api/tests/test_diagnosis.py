"""
Pytest-style version of test_diagnosis.py
"""
import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient, Visit, Consult, Diagnosis
from api.serializers import DiagnosisSerializer
import api.tests.dummies as dummy


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
def consult(visit, test_user):
    """Create a test consult"""
    return Consult.objects.create(
        visit=visit,
        date=timezone.make_aware(
            datetime.fromisoformat(dummy.post_consult_dummy.get("date"))
        ),
        doctor=test_user,
        past_medical_history=dummy.post_consult_dummy.get("past_medical_history"),
        consultation=dummy.post_consult_dummy.get("consultation"),
        plan=dummy.post_consult_dummy.get("plan"),
        referred_for=dummy.post_consult_dummy.get("referred_for"),
        referral_notes=dummy.post_consult_dummy.get("referral_notes"),
        remarks=dummy.post_consult_dummy.get("remarks"),
    )


@pytest.mark.django_db
def test_diagnosis_api_crud_operations(api_client, consult):
    """Test full CRUD lifecycle for diagnosis endpoint"""
    list_endpoint = "diagnosis:diagnosis_list"
    detail_endpoint = "diagnosis:diagnosis_pk"
    
    # DiagnosisSerializer expects a `consult_id` field for input
    diagnosis_data = {
        "consult_id": consult.id,
        "details": dummy.post_diagnosis_dummy.get("details"),
        "category": dummy.post_diagnosis_dummy.get("category"),
    }

    # POST - Create diagnosis
    post_response = api_client.post(reverse(list_endpoint), diagnosis_data)
    assert post_response.status_code == 201
    expected = DiagnosisSerializer(Diagnosis.objects.get(pk=1)).data
    assert post_response.data == expected

    # GET - Retrieve diagnosis
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected

    # PATCH - Update diagnosis
    put_response = api_client.patch(reverse(detail_endpoint, args=["1"]), diagnosis_data)
    assert put_response.status_code == 200
    assert put_response.data == expected

    # GET - Verify update
    get_response = api_client.get(reverse(detail_endpoint, args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected

    # DELETE - Remove diagnosis
    delete_response = api_client.delete(reverse(detail_endpoint, args=["1"]))
    assert delete_response.status_code == 204
    assert delete_response.data == {"message": "Deleted successfully"}

    # GET list - Verify deletion
    get_response = api_client.get(reverse(list_endpoint))
    assert get_response.status_code == 200
    assert get_response.data == []
