"""GET tests for patients resource."""

import pytest
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from api.tests.factories import patient_payloads

# Tiny PNG
_TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.mark.django_db
def test_patients_get_SingleAndList(api_client, patient_instance):
    """Test retrieving patients via GET - single and list"""
    # single
    response = api_client.get(
        reverse("patients:patients_pk", args=[patient_instance.pk])
    )
    assert response.status_code == 200

    # list
    response = api_client.get(reverse("patients:patients_list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["pk"] == patient_instance.pk


@pytest.mark.django_db
def test_patients_get_NonexistentReturns200(api_client):
    """Edge case - get nonexistent patient"""
    response = api_client.get(reverse("patients:patients_pk", args=["99999"]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_patients_get_FiltersByNameAndVillage(api_client):
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


@pytest.mark.django_db
def test_patients_get_NameCaseInsensitive(api_client):
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    base = patient_payloads(picture=None, offline_picture=uploaded)[0]
    base = {**base, "name": "alice"}
    resp = api_client.post(reverse("patients:patients_list"), base)
    assert resp.status_code in (200, 201)

    resp = api_client.get(reverse("patients:patients_list") + "?name=ALICE")
    assert resp.status_code == 200
    assert any(p.get("name") == "alice" for p in resp.data)


@pytest.mark.django_db
def test_patients_get_CombinedFilters(api_client):
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
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
def test_patients_get_NoMatchReturnsEmpty(api_client):
    resp = api_client.get(
        reverse("patients:patients_list") + "?name=this_should_not_exist"
    )
    assert resp.status_code == 200
    assert resp.data == []


@pytest.mark.django_db
def test_patients_get_MultipleMatchesReturned(api_client):
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    base = patient_payloads(picture=None, offline_picture=uploaded)[0].copy()
    vp = base["village_prefix"]
    for i in range(3):
        p = {**base, "name": f"multi{i}"}
        r = api_client.post(reverse("patients:patients_list"), p)
        assert r.status_code in (200, 201)

    resp = api_client.get(reverse("patients:patients_list") + f"?village_code={vp}")
    assert resp.status_code == 200
    matches = [p for p in resp.data if p.get("village_prefix") == vp]
    assert len(matches) >= 3


@pytest.mark.django_db
def test_patients_get_UnknownParamIgnored(api_client):
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    payloads = patient_payloads(picture=None, offline_picture=uploaded)
    for p in payloads[:2]:
        r = api_client.post(reverse("patients:patients_list"), p)
        assert r.status_code in (200, 201)

    resp = api_client.get(reverse("patients:patients_list") + "?unknown_param=foo")
    assert resp.status_code == 200
    assert len(resp.data) >= 2
