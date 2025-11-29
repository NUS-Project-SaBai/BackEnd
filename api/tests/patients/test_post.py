"""POST tests for patients resource."""

import pytest
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import Patient
from api.serializers import PatientSerializer
from api.tests.factories import patient_payloads

# Keep a tiny PNG locally to avoid importing from sibling modules
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.mark.django_db
def test_patients_post_SuccessCreate(api_client):
    """Test creating patients via POST - success and edge cases"""
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    payload = patient_payloads(picture=None, offline_picture=uploaded)[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200

    patient = Patient.objects.get(pk=1)
    expected = PatientSerializer(patient).data
    assert response.data == expected

    # Edge case - empty patient data
    response = api_client.post(reverse("patients:patients_list"), {})
    assert response.status_code == 400


@pytest.mark.django_db
def test_patients_post_MissingRequiredFields(api_client):
    """POST should fail when required fields are missing."""
    base = patient_payloads()[0].copy()
    base.pop("picture", None)
    base.pop("offline_picture", None)

    # Missing name
    missing_name = base.copy()
    missing_name.pop("name", None)
    resp = api_client.post(reverse("patients:patients_list"), missing_name)
    assert resp.status_code == 400
    assert resp.data.get("error") == "Missing name"

    # Missing village_prefix
    missing_village = base.copy()
    missing_village.pop("village_prefix", None)
    resp = api_client.post(reverse("patients:patients_list"), missing_village)
    assert resp.status_code == 400
    assert resp.data.get("error") == "Missing village_prefix"

    # Missing gender
    missing_gender = base.copy()
    missing_gender.pop("gender", None)
    resp = api_client.post(reverse("patients:patients_list"), missing_gender)
    assert resp.status_code == 400
    assert resp.data.get("error") == "Missing gender"
