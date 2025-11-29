"""
Test patient API endpoints - organized by HTTP method with edge cases
"""

import pytest
from rest_framework.reverse import reverse

from api.models import Patient
from api.serializers import PatientSerializer
import api.tests.dummies as dummy
from api.tests.factories import patient_payloads
from django.core.files.uploadedfile import SimpleUploadedFile

# Tiny PNG used for in-memory uploaded files in tests
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.fixture
def patient_instance(api_client):
    """Create a patient instance for tests that need existing data"""
    # Provide an in-memory uploaded offline picture so model validation passes
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    payload = patient_payloads(picture=None, offline_picture=uploaded)[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200
    return Patient.objects.get(pk=1)


@pytest.mark.django_db
def test_patient_post(api_client):
    """Test creating patients via POST - success and edge cases"""
    # Successful case - create patient
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    payload = patient_payloads(picture=None, offline_picture=uploaded)[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200

    patient = Patient.objects.get(pk=1)
    expected = PatientSerializer(patient).data
    assert response.data == expected

    # Edge case - empty patient data
    response = api_client.post(reverse("patients:patients_list"), {})
    # Real API validates required fields; expect 400 for empty payload
    assert response.status_code == 400


@pytest.mark.django_db
def test_patient_get(api_client, patient_instance):
    """Test retrieving patients via GET - single, list, and edge cases"""
    # Successful case - retrieve single patient by pk
    response = api_client.get(
        reverse("patients:patients_pk", args=[patient_instance.pk])
    )
    assert response.status_code == 200

    # Successful case - list patients
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["pk"] == patient_instance.pk

    # Edge case - get nonexistent patient
    response = api_client.get(reverse("patients:patients_pk", args=["99999"]))
    assert response.status_code == 200  # API returns 200 for nonexistent


@pytest.mark.django_db
def test_patient_patch(api_client, patient_instance):
    """Test updating patients via PATCH - success and edge cases"""
    # Successful case - update patient
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
def test_patient_delete(api_client, patient_instance):
    """Test deleting patients via DELETE - success and edge cases"""
    patient_pk = patient_instance.pk

    # Successful case - delete patient
    response = api_client.delete(reverse("patients:patients_pk", args=[patient_pk]))
    assert response.status_code == 200
    assert response.data == {"message": "Deleted successfully"}

    # Verify patient is gone from list
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert response.data == []

    # Edge case - delete already deleted patient (should 404)
    response = api_client.delete(
        reverse("patients:patients_pk", args=[str(patient_pk)])
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_patient_post_missing_required_fields(api_client, settings):
    """POST should fail when required fields are missing."""

    base = patient_payloads()[0].copy()
    # Remove any string `picture` values so offline tests don't trigger
    # DRF ImageField validation (we only want to test missing required fields).
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


@pytest.mark.django_db
def test_patient_list_filters(api_client):
    """Create two patients and test list filters by name and village_code."""
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    base_payload = patient_payloads(picture=None, offline_picture=uploaded)
    r1 = api_client.post(reverse("patients:patients_list"), base_payload[0])
    assert r1.status_code in (200, 201)
    r2 = api_client.post(reverse("patients:patients_list"), base_payload[1])
    assert r2.status_code in (200, 201)

    # filter by village_code
    resp = api_client.get(
        reverse("patients:patients_list")
        + f"?village_code={base_payload[0]['village_prefix']}"
    )
    assert resp.status_code == 200
    assert any(
        p.get("village_prefix") == base_payload[0]["village_prefix"] for p in resp.data
    )

    # filter by name
    resp = api_client.get(
        reverse("patients:patients_list") + f"?name={base_payload[1]['name']}"
    )
    assert resp.status_code == 200
    assert any(p.get("name") == base_payload[1]["name"] for p in resp.data)

    # Edge case - delete nonexistent patient
    response = api_client.delete(reverse("patients:patients_pk", args=["99999"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_patient_patch_update_fields(api_client, patient_instance):
    """PATCH should allow partial updates of simple fields."""
    pk = patient_instance.pk
    payload = {"name": "patched_name", "contact_no": "+1234567890"}
    resp = api_client.patch(reverse("patients:patients_pk", args=[pk]), payload)
    assert resp.status_code == 200
    assert resp.data["name"] == "patched_name"
    assert resp.data["contact_no"] == "+1234567890"


@pytest.mark.django_db
def test_patient_patch_update_offline_picture(api_client, patient_instance):
    """PATCH can replace an offline picture using multipart upload."""
    pk = patient_instance.pk
    uploaded = SimpleUploadedFile("new.png", _TINY_PNG, content_type="image/png")
    resp = api_client.patch(
        reverse("patients:patients_pk", args=[pk]), {"offline_picture": uploaded}
    )
    assert resp.status_code == 200
    # Backend should have saved the offline picture on the model
    p = Patient.objects.get(pk=pk)
    assert p.offline_picture and getattr(p.offline_picture, "name", "") != ""


@pytest.mark.django_db
def test_patient_patch_invalid_date_of_birth(api_client, patient_instance):
    """Invalid date_of_birth should produce a 400 validation error."""
    pk = patient_instance.pk
    resp = api_client.patch(
        reverse("patients:patients_pk", args=[pk]), {"date_of_birth": "not-a-date"}
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_patient_patch_no_changes(api_client, patient_instance):
    """PATCH with empty payload should be a no-op and return current resource."""
    pk = patient_instance.pk
    # Capture current representation
    before = PatientSerializer(patient_instance).data
    resp = api_client.patch(reverse("patients:patients_pk", args=[pk]), {})
    assert resp.status_code == 200
    assert resp.data == before


@pytest.mark.django_db
def test_patient_filter_name_case_insensitive(api_client):
    """Name filter should be case-insensitive (uses iexact)."""
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    base = patient_payloads(picture=None, offline_picture=uploaded)[0]
    # ensure lowercase stored name
    base = {**base, "name": "alice"}
    resp = api_client.post(reverse("patients:patients_list"), base)
    assert resp.status_code in (200, 201)

    # query with different case
    resp = api_client.get(reverse("patients:patients_list") + "?name=ALICE")
    assert resp.status_code == 200
    assert any(p.get("name") == "alice" for p in resp.data)


@pytest.mark.django_db
def test_patient_filters_combined(api_client):
    """Combined filters should apply as an AND (both must match)."""
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    # Create three patients such that only one matches both name+village
    p0 = patient_payloads(picture=None, offline_picture=uploaded)[0].copy()
    p1 = patient_payloads(picture=None, offline_picture=uploaded)[0].copy()
    p2 = patient_payloads(picture=None, offline_picture=uploaded)[0].copy()

    p0.update({"village_prefix": "COMB", "name": "COMBNAME"})
    p1.update({"village_prefix": "OTHER", "name": "COMBNAME"})
    p2.update({"village_prefix": "COMB", "name": "OTHERNAME"})

    for payload in (p0, p1, p2):
        r = api_client.post(reverse("patients:patients_list"), payload)
        assert r.status_code in (200, 201)

    query = f"?name={p0['name']}&village_code={p0['village_prefix']}"
    resp = api_client.get(reverse("patients:patients_list") + query)
    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]["name"] == p0["name"]


@pytest.mark.django_db
def test_patient_filter_no_match(api_client):
    """Querying with values that match nothing should return an empty list."""
    resp = api_client.get(
        reverse("patients:patients_list") + "?name=this_should_not_exist"
    )
    assert resp.status_code == 200
    assert resp.data == []


@pytest.mark.django_db
def test_patient_filter_multiple_matches(api_client):
    """Filter should return all matching records when multiple exist."""
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    base = patient_payloads(picture=None, offline_picture=uploaded)[0].copy()
    # create three patients sharing the same village_prefix
    vp = base["village_prefix"]
    for i in range(3):
        p = {**base, "name": f"multi{i}"}
        r = api_client.post(reverse("patients:patients_list"), p)
        assert r.status_code in (200, 201)

    resp = api_client.get(reverse("patients:patients_list") + f"?village_code={vp}")
    assert resp.status_code == 200
    matches = [p for p in resp.data if p.get("village_prefix") == vp]
    assert len(matches) >= 3
