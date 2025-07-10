from django.urls import path
from api.views import FileView
from api.views import PdfConsultView

urlpatterns = [
    path("upload", FileView.as_view(), name="upload_file"),
    path("pdf_consults/<int:pk>", PdfConsultView.as_view(), name="pdf_consults_pk"),
]
