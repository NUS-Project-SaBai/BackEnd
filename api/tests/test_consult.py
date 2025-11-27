"""
Pytest-style version of test_consult.py
"""

import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.reverse import reverse

from api.models import Patient, Visit, Consult
from api.serializers import ConsultSerializer
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


@pytest.mark.django_db
class TestConsultAPIPytest:
    """Pytest-style consult API test (for comparison with unittest version)"""
    
    def test_consult_crud_operations(self, api_client, visit, test_user):
        """Test full CRUD lifecycle for consult endpoint"""
        # POST - Create consult
        post_response = api_client.post(
            reverse("consults:consults_list"),
            {"consult": dummy.post_consult_dummy},
            HTTP_DOCTOR=test_user.email,
        )
        assert post_response.status_code == 201
        expected = ConsultSerializer(Consult.objects.get(pk=1)).data
        assert post_response.data == expected

        # GET - Retrieve consult
        get_response = api_client.get(reverse("consults:consults_pk", args=["1"]))
        assert get_response.status_code == 200
        expected = ConsultSerializer(Consult.objects.get(pk=1)).data
        assert get_response.data == expected

        # PATCH - Update consult
        put_response = api_client.patch(
            reverse("consults:consults_pk", args=["1"]),
            {"consult": dummy.post_consult_dummy},
            HTTP_DOCTOR=test_user.email,
        )
        assert put_response.status_code == 200
        expected = ConsultSerializer(Consult.objects.get(pk=1)).data
        assert put_response.data == expected

        # GET - Verify update
        get_response = api_client.get(reverse("consults:consults_pk", args=["1"]))
        assert get_response.status_code == 200
        expected = ConsultSerializer(Consult.objects.get(pk=1)).data
        assert get_response.data == expected

        # DELETE - Remove consult
        delete_response = api_client.delete(reverse("consults:consults_pk", args=["1"]))
        assert delete_response.status_code == 204
        assert delete_response.data == {"message": "Deleted successfully"}

        # GET list - Verify deletion
        get_response = api_client.get(reverse("consults:consults_list") + "?visit=1")
        assert get_response.status_code == 200
        assert get_response.data == []


# Alternative: function-based test (even more concise)
@pytest.mark.django_db
def test_consult_api_function_style(api_client, visit, test_user):
    """Same test as above, but as a plain function instead of class method"""
    # POST
    post_response = api_client.post(
        reverse("consults:consults_list"),
        {"consult": dummy.post_consult_dummy},
        HTTP_DOCTOR=test_user.email,
    )
    assert post_response.status_code == 201
    
    consult = Consult.objects.get(pk=1)
    expected = ConsultSerializer(consult).data
    assert post_response.data == expected
    
    # GET
    get_response = api_client.get(reverse("consults:consults_pk", args=["1"]))
    assert get_response.status_code == 200
    assert get_response.data == expected
    
    # DELETE
    delete_response = api_client.delete(reverse("consults:consults_pk", args=["1"]))
    assert delete_response.status_code == 204
    assert delete_response.data == {"message": "Deleted successfully"}
