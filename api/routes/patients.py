from django.urls import path
from api.views import PatientView, PatientSearchView, PdfAllReportView
from api.views.pdf_patient_report_view import PdfPatientReportView

urlpatterns = [
    path("", PatientView.as_view(), name="patients_list"),
    path("<int:pk>/", PatientView.as_view(), name="patients_pk"),
    path("search_face/", PatientSearchView.as_view(), name="patients_list"),
    # report_type is either latest_consult or all_consults
    path(
        "<int:patient_id>/reports/pdf/<str:report_type>/",
        PdfPatientReportView.as_view(),
        name="latest_patient_pdf_report",
    ),
]
