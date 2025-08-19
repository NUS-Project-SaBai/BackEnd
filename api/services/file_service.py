# api/services/files.py

from api.models import File
from api.serializers import FileSerializer
from api.utils import file_utils
from django.conf import settings


def list_files(patient_pk=None, include_deleted=False):
    files = File.objects.all()
    if patient_pk:
        files = files.filter(patient_id=patient_pk)
    if not include_deleted:
        files = files.filter(is_deleted=False)
    return FileSerializer(files, many=True).data


def get_file(pk):
    file = File.objects.get(pk=pk)
    return FileSerializer(file).data


def create_file(uploaded_file, labeled_filename, patient_pk, description: str | None = None):
    if not uploaded_file:
        raise ValueError("No file was uploaded")
    if not labeled_filename:
        raise ValueError("No labeled filename provided")

    data = {
        "patient": patient_pk,
        "file_name": labeled_filename,
    }
    if description is not None:
        data["description"] = description

    if settings.OFFLINE:
        data["offline_file"] = uploaded_file
    else:
        data["file_path"] = file_utils.upload_file(uploaded_file, labeled_filename)

    serializer = FileSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    obj = serializer.save()
    return FileSerializer(obj).data


def update_file(pk, data):
    file = File.objects.get(pk=pk)
    serializer = FileSerializer(file, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    obj = serializer.save()
    return FileSerializer(obj).data

#soft delete only
def delete_file(pk):
    file = File.objects.get(pk=pk)
    if not file.is_deleted:
        file.is_deleted = True
        file.save(update_fields=["is_deleted"])
    return FileSerializer(file).data

def restore_file(pk):
    file = File.objects.get(pk=pk)
    if file.is_deleted:
        file.is_deleted = False
        file.save(update_fields=["is_deleted"])
    return FileSerializer(file).data