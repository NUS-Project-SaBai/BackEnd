from api.serializers.visit_serializer import VisitSerializer
from api.types.patient_types import PatientAPIData
from api.serializers.patient_serializer import PatientSerializer
from api.services import visit_service, vitals_service
from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, OFFLINE
from api.utils import facial_recognition
from api.models import Patient
from django.db import transaction


def extract_and_clean_picture(patientData: PatientAPIData, pictureData):
    """
    Handles separation of 'picture' field based on OFFLINE mode.
    """
    if OFFLINE:
        if pictureData:
            patientData["offline_picture"] = pictureData
        patientData.pop("picture", None)
    else:
        patientData["picture"] = pictureData
    return patientData


def generate_face_encoding(data):
    """
    Returns face encoding if recognition is enabled.
    """
    if not ENABLE_FACIAL_RECOGNITION:
        return ""
    picture = data.get("offline_picture") if OFFLINE else data.get("picture")
    return facial_recognition.generate_faceprint(picture)


def search_patients_by_face(picture):
    """
    - Run facial recognition on the provided image
    - Find patients with matching face encodings
    - Return (patients queryset, confidence dict)
    """
    face_encoding = facial_recognition.search_faceprint(picture)
    matched_encodings = list(face_encoding.keys())
    patients = Patient.objects.filter(face_encodings__in=matched_encodings)
    return patients, face_encoding


@transaction.atomic
def create_patient_with_vitals(
    patientData: PatientAPIData, face_encoding: str, vitalsData
):
    patient_serializer: PatientSerializer = PatientSerializer(data=patientData)
    patient_serializer.is_valid(raise_exception=True)
    created_patient: Patient = patient_serializer.save(face_encodings=face_encoding)

    # Create Visit
    visit_serializer: VisitSerializer = visit_service.create_visit(
        {"patient_id": created_patient.pk, "status": "started"}
    )
    created_visit = visit_serializer.instance

    # Create vitals with temperature
    vitalsData["visit_id"] = created_visit.pk
    vitals_service.create_vitals(vitalsData)

    return patient_serializer
