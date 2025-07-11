# api/services/files.py

from api.models import File
from api.serializers import FileSerializer
from BackEnd.api.utils import file_utils
from django.conf import settings


def list_files(patient_pk=None):
    files = File.objects.all()
    if patient_pk:
        files = files.filter(patient_id=patient_pk)
    return FileSerializer(files, many=True).data


def get_file(pk):
    file = File.objects.get(pk=pk)
    return FileSerializer(file).data


def create_file(uploaded_file, labeled_filename, patient_pk):
    if not uploaded_file:
        raise ValueError("No file was uploaded")
    if not labeled_filename:
        raise ValueError("No labeled filename provided")

    data = {
        "patient": patient_pk,
        "file_name": labeled_filename,
    }

    if settings.OFFLINE:
        data["offline_file"] = uploaded_file
    else:
        data["file_path"] = file_utils.upload_file(uploaded_file, labeled_filename)

    serializer = FileSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def update_file(pk, data):
    file = File.objects.get(pk=pk)
    serializer = FileSerializer(file, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_file(pk):
    File.objects.get(pk=pk).delete()
