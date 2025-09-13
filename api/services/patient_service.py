from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, OFFLINE
from api.utils import facial_recognition
from api.models import Patient


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
