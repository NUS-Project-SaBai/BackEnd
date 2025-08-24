from django.urls import path
from api.views.patient_consult_view import PatientConsultView

urlpatterns = [
    path("", PatientConsultView.as_view(), name="patient_consult"),
]
