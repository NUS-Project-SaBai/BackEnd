from django.urls import path
from api.views import FileView
from api.views import PdfConsultView

urlpatterns = [
    path("", FileView.as_view(), name="files"),
    path(
        "<int:pk>/", FileView.as_view(), name="file_detail"
    ),  # Individual file operations
]
