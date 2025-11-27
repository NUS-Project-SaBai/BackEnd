# api/services/files.py

from typing import NamedTuple

from django.conf import settings
from django.core.files import File as DjangoFileType
from django.db.models.query import QuerySet

from api.models import File
from api.models.patient_model import Patient
from django.shortcuts import get_object_or_404
from api.serializers import FileSerializer
from api.utils import file_utils


def list_files(patient_pk: int = None, is_deleted: bool = None) -> QuerySet[File]:
    """
    List files with optional filtering by patient_pk and is_deleted status.

    Args:
        patient_pk (int | None, optional): Find files associated with patient's pk.
            None matches all patient's pk. Defaults to None.
        is_deleted (bool | None, optional): Filter by deletion status.
            None will match all files. Defaults to None.
    Returns:
        QuerySet: Filtered list of File objects.
    """
    files = File.objects.all()

    if is_deleted is not None:
        files = files.filter(is_deleted=is_deleted)

    if patient_pk is not None:
        files = files.filter(patient_id=patient_pk)
    return files


def get_file(pk):
    file = File.objects.get(pk=pk)
    return FileSerializer(file).data


def list_patient_uploads(patient_pks: list[int] = None, is_deleted: bool = None):
    """
    Returns a list of Upload objects (patient + their files).
    If patient_pks is None, groups all files by their patient.
    """
    from collections import defaultdict

    files = list_files(is_deleted=is_deleted)

    # Filter by specific patients if provided
    if patient_pks:
        files = files.filter(patient_id__in=patient_pks)

    # Group files by patient
    patient_files_map = defaultdict(list)
    patient_ids = set()

    for file in files:
        if file.patient_id:
            patient_files_map[file.patient_id].append(file)
            patient_ids.add(file.patient_id)

    # Fetch all patients at once
    patients = Patient.objects.filter(pk__in=patient_ids)
    patient_map = {p.pk: p for p in patients}

    # Build list of {patient, files} dicts
    uploads = []
    for patient_id, file_list in patient_files_map.items():
        if patient_id in patient_map:
            uploads.append({"patient": patient_map[patient_id], "files": file_list})

    return uploads


def get_patient_upload(patient_pk: int, is_deleted: bool = None):
    """
    Returns a dict with patient instance and filtered files queryset for that patient.
    """
    patient = get_object_or_404(Patient, pk=patient_pk)
    files = list_files(patient_pk=patient_pk, is_deleted=is_deleted)
    return {"patient": patient, "files": files}


def create_files(
    files: list[DjangoFileType],
    descriptions: list[str],
    patient_pk: str,
):
    # throw error when patient_pk is empty or doesn't exists
    if patient_pk.strip() == "" or not Patient.objects.filter(pk=patient_pk).exists():
        raise ValueError(f"Invalid patient {patient_pk}")
    invalid_files = validate_files(files)
    if len(invalid_files) > 0:
        raise ValueError(
            f"""Invalid Files:\n
            {"\n".join(map(
                lambda invalid_file: f'{invalid_file.file.name} \
                    - {invalid_file.error}', invalid_files))}
            """
        )

    created_filenames = []
    for file, description in zip(files, descriptions):
        data = {
            "patient_id": patient_pk,
            "file_name": file.name,
            "description": description,
        }

        if settings.OFFLINE:
            data["offline_file"] = file
        else:
            data["file_path"] = file_utils.upload_files(file, file.name)

        serializer = FileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        created_filenames.append(serializer.save().file_name)
    return created_filenames


InvalidFileItem = NamedTuple(
    "InvalidFileItem", [("file", DjangoFileType), ("error", str)]
)


def validate_files(files: list[DjangoFileType]) -> list[InvalidFileItem]:
    if len(files) == 0:
        raise ValueError("No file was uploaded")
    invalid_files: list[InvalidFileItem] = []
    for file in files:
        if file.name.strip() == "":
            invalid_files.append(InvalidFileItem(file=file, error="No name provided"))
        if file.size > 26214400:  # 25mb
            invalid_files.append(InvalidFileItem(file=file, error="File is too large!"))
    return invalid_files


def update_file(pk, data):
    file = File.objects.get(pk=pk)
    serializer = FileSerializer(file, data=data, partial=True)
    serializer.is_valid(raise_exception=True)

    if not settings.OFFLINE:
        if not file.file_path:
            raise ConnectionError("Failed to edit file on Google Drive.\nFile:\n", file)

        if serializer.validated_data.get("file_name"):
            file_utils.rename_file(
                file.file_path, serializer.validated_data["file_name"]
            )
    return serializer.save()


# soft delete only
def delete_file(pk):
    file = File.objects.get(pk=pk)
    if not file.is_deleted:
        file.is_deleted = True
        file.save(update_fields=["is_deleted"])
    return file


def restore_file(pk):
    file = File.objects.get(pk=pk)
    if file.is_deleted:
        file.is_deleted = False
        file.save(update_fields=["is_deleted"])
    return file
