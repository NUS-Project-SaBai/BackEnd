from django.urls import path
from api.views.patient_records_view import PatientRecordsView

urlpatterns = [
    path("patient-records/", PatientRecordsView.as_view(), name="patient-records"),
]
