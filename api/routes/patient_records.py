from django.urls import path
from api.views.patient_records_view import PatientRecordsView

urlpatterns = [
    path("", PatientRecordsView.as_view(), name="patient_records"),
]
