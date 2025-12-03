"""
PATCH tests for vitals
"""

import pytest
from rest_framework.reverse import reverse
from api.serializers.vitals_serializer import VitalsSerializer
from api.tests.factories import vitals_payloads


@pytest.mark.django_db
def test_vitals_patch_SuccessUpdate(api_client, vitals_instance):
    """Test updating vitals via PATCH - success and edge cases"""
    # Successful case - update vitals
    payload = vitals_payloads()[0]
    response = api_client.patch(
        reverse("vitals:vitals_pk", args=[str(vitals_instance.pk)]),
        payload,
    )
    assert response.status_code in (200, 202)
    numeric_fields = [
        "weight",
        "height",
        "temperature",
        "systolic",
        "diastolic",
        "heart_rate",
        "hemocue_count",
        "blood_glucose_non_fasting",
        "blood_glucose_fasting",
        "pubarche_age",
        "menarche_age",
        "thelarche_age",
        "voice_change_age",
        "testicular_growth_age",
    ]
    assert (
        response.data.get("visit_id", response.data.get("visit")) == payload["visit_id"]
    )
    for key, val in payload.items():
        if key in numeric_fields:
            resp_val = response.data.get(key)
            try:
                if resp_val is None or val is None:
                    assert resp_val == val
                    continue
                assert abs(float(resp_val) - float(val)) < 1e-5
            except Exception:
                assert str(resp_val) == str(val)
        else:
            assert str(response.data.get(key)) == str(val)

    # Edge case - update nonexistent vitals
    response = api_client.patch(reverse("vitals:vitals_pk", args=["99999"]), payload)
    assert response.status_code == 404
