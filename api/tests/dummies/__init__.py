from .patient import post_patient_dummy
from .visit import post_visit_dummy
from .vitals import post_vitals_dummy
from .consult import post_consult_dummy
from .diagnosis import post_diagnosis_dummy
from .medication import post_medication_dummy
from .order import post_order_dummy

__all__ = [
    "post_patient_dummy",
    "post_visit_dummy",
    "post_vitals_dummy",
    "post_consult_dummy",
    "post_diagnosis_dummy",
    "post_medication_dummy",
    "post_order_dummy",
]
