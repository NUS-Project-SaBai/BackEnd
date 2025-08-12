from django.urls import path
from api.views import FileView
from api.views import PdfConsultView

urlpatterns = [
    path("upload/", FileView.as_view(), name="upload_file"),
    path("<int:pk>/", FileView.as_view(), name="file_detail"), # Route for individual file operations
]
