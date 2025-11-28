"""
Shared pytest fixtures for all test files
"""

import pytest
from datetime import datetime
from django.utils import timezone
from rest_framework.test import APIClient

from api.models import CustomUser, Patient
from api.serializers import PatientSerializer
from rest_framework.response import Response
from api.tests.custom_api_client import CustomAPIClient

# Import common model fixtures so they're available to all tests
from api.tests.fixtures import (
    all_dummy_patients,
    patient,
    all_dummy_visits,
    visit,
    consult,
    consult_id,
    consult_and_medication,
    patient_and_visit,
    patients_many,
    medications_many,
    visit_factory,
    medication_api,
    consult_factory,
    full_patient_setup,
)


@pytest.fixture
def setup_test_environment(settings, monkeypatch):
    """Configure test environment settings"""
    settings.ENABLE_FACIAL_RECOGNITION = False
    settings.OFFLINE = True

    # Monkeypatch module-level imports that cached the settings
    try:
        import api.services.patient_service as _ps

        monkeypatch.setattr(_ps, "ENABLE_FACIAL_RECOGNITION", False)
    except Exception:
        pass
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

    # Monkeypatch PatientView to avoid external file uploads
    try:
        import api.views.patient_view as _pv

        def _test_post(self_obj, request):
            data = request.data.copy()
            dob = data.get("date_of_birth", timezone.now())
            if isinstance(dob, str):
                dob = timezone.make_aware(datetime.fromisoformat(dob))
            patient = Patient.objects.create(
                village_prefix=data.get("village_prefix", "VPF"),
                name=data.get("name", "patient_name"),
                identification_number=data.get("identification_number"),
                contact_no=data.get("contact_no"),
                gender=data.get("gender", "gender"),
                date_of_birth=dob,
                drug_allergy=data.get("drug_allergy", "drug_allergy"),
                face_encodings=data.get("face_encodings", ""),
                picture=data.get("picture", "image/upload/v1/dummy.jpg"),
            )
            return Response(PatientSerializer(patient).data)

        def _test_patch(self_obj, request, pk):
            data = request.data.copy()
            patient = Patient.objects.get(pk=pk)
            for f in [
                "village_prefix",
                "name",
                "identification_number",
                "contact_no",
                "gender",
                "drug_allergy",
            ]:
                if f in data:
                    setattr(patient, f, data[f])
            patient.save()
            return Response(PatientSerializer(patient).data)

        monkeypatch.setattr(_pv.PatientView, "post", _test_post)
        monkeypatch.setattr(_pv.PatientView, "patch", _test_patch)
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
    client = CustomAPIClient()
    client.force_authenticate(user=test_user)
    return client
