from django.urls import path
from api.views import ConsultView
from api.views import PdfConsultView

urlpatterns = [
    path("", ConsultView.as_view(), name="consults_list"),
    path("<int:pk>/", ConsultView.as_view(), name="consults_pk"),
    path("<int:pk>/pdf", PdfConsultView.as_view(), name="pdf_consults_pk"),
    path("pdf/", PdfConsultView.as_view(), name="pdf_consults"),
]
