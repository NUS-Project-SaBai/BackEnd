from api.serializers.patient_serializer import PatientSerializer
from api.serializers.vitals_serializer import VitalsSerializer
from api.services import visit_service, vitals_service
from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, OFFLINE
from api.utils import facial_recognition
from api.models import Patient
from django.db import transaction


def extract_and_clean_picture(data):
    """
    Handles separation of 'picture' field based on OFFLINE mode.
    """
    if OFFLINE:
        picture = data.get("picture", None)
        if picture:
            data["offline_picture"] = picture
        data.pop("picture", None)
    return data


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
def create_patient_with_temperature(data, face_encoding):
    patient_serializer = PatientSerializer(data=data)
    if patient_serializer.is_valid(raise_exception=True):
        patient_serializer.save(face_encodings=face_encoding)

    # Create Visit
    visit = visit_service.create_visit(
        {'patient_id': patient_serializer.data.get("pk"),
         'status': 'started'}
    )

    temperature = data.get("temperature")
    if (temperature):
        # Create vitals with temperature
        patient_serializer = VitalsSerializer(data=
            {"visit_id": visit.pk,
            "temperature": temperature}
        )
        patient_serializer.is_valid(raise_exception=True)
        vitals = patient_serializer.save()

    return patient_serializer