"""
Shared pytest fixtures for all test files
"""


import pytest

from api.models import CustomUser
from api.tests.custom_api_test_client import CustomAPITestClient

# Import common model fixtures so they're available to all tests
from api.tests.fixtures import *


@pytest.fixture
def setup_test_environment(settings, monkeypatch):
    """Configure test environment settings"""
    settings.ENABLE_FACIAL_RECOGNITION = False
    settings.OFFLINE = True

    # Monkeypatch module-level imports that cached the settings
    try:
        import api.services.patient_service as _ps

        # Ensure module-level flags in patient_service reflect test settings
        monkeypatch.setattr(_ps, "ENABLE_FACIAL_RECOGNITION", False)
        monkeypatch.setattr(_ps, "OFFLINE", True)
    except Exception:
        pass
    # Do not monkeypatch PatientView or Patient.save here; allow view+serializer
    # to run. We'll relax ImageField validation so tests can send multipart
    # uploads without requiring Pillow.
    try:
        import api.utils.facial_recognition as _fr

        monkeypatch.setattr(_fr, "ENABLE_FACIAL_RECOGNITION", False)
    except Exception:
        pass
    try:
        import api.views.patient_search_view as _psv

        monkeypatch.setattr(_psv, "ENABLE_FACIAL_RECOGNITION", False)
    except Exception:
        pass
    try:
        import api.utils.doctor_utils as _du

        monkeypatch.setattr(_du, "OFFLINE", True)
    except Exception:
        pass

    # Stub facial recognition functions
    try:
        import api.utils.facial_recognition as _fr

        monkeypatch.setattr(_fr, "generate_faceprint", lambda file: "")
        monkeypatch.setattr(_fr, "search_faceprint", lambda file: {})
    except Exception:
        pass

    # Stub cloudinary uploader
    try:
        import cloudinary.uploader as _u

        monkeypatch.setattr(
            _u, "upload", lambda *args, **kwargs: {"url": "image/upload/v1/dummy.jpg"}
        )
    except Exception:
        pass

    # Relax ImageField validation so tests can send multipart files without
    # installing Pillow. This monkeypatch makes ImageField.clean a no-op.
    try:
        from django.db.models.fields.files import ImageField as _ImageField

        monkeypatch.setattr(
            _ImageField,
            "clean",
            lambda self, value, model_instance=None: value,
            raising=False,
        )
    except Exception:
        pass
    try:
        from rest_framework import serializers as _drf_serializers

        # Bypass DRF ImageField validation in tests (avoid Pillow requirement)
        monkeypatch.setattr(
            _drf_serializers.ImageField,
            "to_internal_value",
            lambda self, data: data,
            raising=False,
        )
    except Exception:
        pass

    # Convert string picture values into in-memory uploaded files so DRF ImageField
    # validators accept them during tests (we still stub actual uploads).
    try:
        from django.core.files.uploadedfile import SimpleUploadedFile
        from rest_framework import serializers as _drf_serializers

        import api.serializers.patient_serializer as _patient_serializer
        import api.services.patient_service as _ps
        import api.views.patient_view as _pv

        _orig_extract = getattr(_ps, "extract_and_clean_picture", None)

        def _test_extract_and_clean_picture(data):
            # Run original extraction to move `picture` -> `offline_picture` when OFFLINE
            if _orig_extract:
                data = _orig_extract(data)
            # If offline_picture is a string (dummy path from fixtures), convert
            # it into a SimpleUploadedFile so ImageField validation passes.
            pic = data.get("offline_picture")
            if isinstance(pic, str) and pic:
                # Use a fixed .png filename to match the PNG bytes we provide
                filename = "test.png"
                # Use a tiny valid PNG payload so DRF ImageField doesn't reject it as empty
                tiny_png = (
                    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
                    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
                    b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc3"
                    b"\x00\x00\x00\x00IEND\xaeB`\x82"
                )
                data["offline_picture"] = SimpleUploadedFile(
                    filename, tiny_png, content_type="image/png"
                )
            return data

        # Patch both the service and the view reference (view imported the function at module import)
        monkeypatch.setattr(
            _ps, "extract_and_clean_picture", _test_extract_and_clean_picture
        )
        monkeypatch.setattr(
            _pv, "extract_and_clean_picture", _test_extract_and_clean_picture
        )
        # Keep extract_and_clean_picture wrapper and cloudinary/facial-recog
        # stubs so tests don't perform real uploads or recognition.
    except Exception:
        pass


@pytest.fixture
def test_user(db, setup_test_environment):
    """Create and return a test user"""
    user = CustomUser.objects.create_user(
        username="test_user",
        email="test@example.com",
        auth0_id="1",
    )
    yield user
    user.delete()


@pytest.fixture
def api_client(test_user):
    """Create an authenticated API client"""
    client = CustomAPITestClient()
    client.force_authenticate(user=test_user)
    return client
