from django.urls import path
from api.views import FileView
from api.views import PdfConsultView

urlpatterns = [
    path("upload/", FileView.as_view(), name="upload_file"),
    path(
        "upload/<int:pk>/", FileView.as_view(), name="upload_file"
    ),  # Route for individual file operations
]
