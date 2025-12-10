from typing import TypedDict, Optional, Any, List

from api.types.vitals_types import VitalsRegistrationAPIData


class PatientAPIData(TypedDict):
    village_prefix: str
    name: str
    identification_number: str
    contact_no: str
    gender: str
    date_of_birth: str
    poor: str
    bs2: str
    sabai: str
    drug_allergy: str
    face_encodings: str
    picture: bytes
    offline_picture: bytes
    is_image_edited: bool
    to_get_report: bool


class RegstriationAPIData(TypedDict):
    patient: PatientAPIData
    vitals: VitalsRegistrationAPIData
    picutre: bytes
