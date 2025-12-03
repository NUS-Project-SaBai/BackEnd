from django.urls import path
from api.views import ConsultView
from api.views import PdfConsultView
from api.views.pdf_all_report_view import PdfAllReportView

urlpatterns = [
    path("", ConsultView.as_view(), name="consults_list"),
    path("<int:pk>/", ConsultView.as_view(), name="consults_pk"),
    path("<int:pk>/pdf", PdfConsultView.as_view(), name="pdf_consults_pk"),
    path("pdf/", PdfConsultView.as_view(), name="pdf_consults"),
    path(
        "reports/pdf/all/", PdfAllReportView.as_view(), name="all_patients_pdf_reports"
    ),
]
