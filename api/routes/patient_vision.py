from django.urls import path
from api.views.patient_vision_view import PatientVisionView

urlpatterns = [
    path("", PatientVisionView.as_view(), name="patient_vision"),
]
