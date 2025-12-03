"""PATCH tests for patients resource."""

import pytest
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import Patient
from api.serializers import PatientSerializer
from api.tests.factories import patient_payloads

# Tiny PNG
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.mark.django_db
def test_patients_patch_SuccessUpdate(api_client, patient_instance):
    """Test updating patients via PATCH - success and edge cases"""
    update_payload = {"name": "updated_name"}
    response = api_client.patch(
        reverse("patients:patients_pk", args=[patient_instance.pk]), update_payload
    )
    assert response.status_code == 200

    patient_instance.refresh_from_db()
    expected = PatientSerializer(patient_instance).data
    assert response.data == expected

    # Edge case - update nonexistent patient
    response = api_client.patch(
        reverse("patients:patients_pk", args=["99999"]), update_payload
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_patients_patch_UpdateFields(api_client, patient_instance):
    pk = patient_instance.pk
    payload = {"name": "patched_name", "contact_no": "+1234567890"}
    resp = api_client.patch(reverse("patients:patients_pk", args=[pk]), payload)
    assert resp.status_code == 200
    assert resp.data["name"] == "patched_name"
    assert resp.data["contact_no"] == "+1234567890"


@pytest.mark.django_db
def test_patients_patch_UpdateOfflinePicture(api_client, patient_instance):
    pk = patient_instance.pk
    uploaded = SimpleUploadedFile("new.png", _TINY_PNG, content_type="image/png")
    resp = api_client.patch(
        reverse("patients:patients_pk", args=[pk]), {"offline_picture": uploaded}
    )
    assert resp.status_code == 200
    p = Patient.objects.get(pk=pk)
    assert p.offline_picture and getattr(p.offline_picture, "name", "") != ""


@pytest.mark.django_db
def test_patients_patch_InvalidDateOfBirthReturns400(api_client, patient_instance):
    pk = patient_instance.pk
    resp = api_client.patch(
        reverse("patients:patients_pk", args=[pk]), {"date_of_birth": "not-a-date"}
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_patients_patch_NoChangesReturnsSame(api_client, patient_instance):
    pk = patient_instance.pk
    before = PatientSerializer(patient_instance).data
    resp = api_client.patch(reverse("patients:patients_pk", args=[pk]), {})
    assert resp.status_code == 200
    assert resp.data == before
