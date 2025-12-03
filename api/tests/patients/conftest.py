import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse

from api.models import Patient
from api.tests.factories import patient_payloads

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
    uploaded = SimpleUploadedFile("test.png", _TINY_PNG, content_type="image/png")
    payload = patient_payloads(picture=None, offline_picture=uploaded)[0]
    response = api_client.post(reverse("patients:patients_list"), payload)
    assert response.status_code == 200
    return Patient.objects.get(pk=1)
