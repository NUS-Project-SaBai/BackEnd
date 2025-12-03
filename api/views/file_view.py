# api/views/file_view.py
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import FileSerializer
from api.serializers.patient_files_serializer import PatientFilesSerializer
from api.services import file_service


class FileView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return Response(file_service.get_file(pk), status=status.HTTP_200_OK)

        patient_pk = request.query_params.get("patient_pk")
        deleted_param = request.query_params.get("deleted", "false")

        deleted_mapping = {"all": None, "true": True, "false": False}
        if deleted_param not in deleted_mapping:
            return Response(
                {"error": "deleted parameter must be 'all', 'true', or 'false'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        is_deleted = deleted_mapping[deleted_param]

        # If a patient_pk is provided, return single PatientFiles object in a list
        if patient_pk:
            payload = file_service.get_patient_files(
                patient_pk=patient_pk, is_deleted=is_deleted
            )
            return Response(
                PatientFilesSerializer([payload], many=True).data,
                status=status.HTTP_200_OK,
            )

        # Otherwise, return list of PatientFiles objects (files grouped by patient)
        patient_files = file_service.list_patient_files(is_deleted=is_deleted)
        return Response(
            PatientFilesSerializer(patient_files, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request):
        try:
            uploaded_files = request.FILES.getlist("files")
            descriptions = request.data.getlist("descriptions")
            patient_pk = request.data.get("patient_pk")

            created_filenames = file_service.create_files(
                uploaded_files,
                descriptions,
                patient_pk if type(patient_pk) == int else int(patient_pk),
            )
            newline = "\n"  # f-string expression part cannot include backslash. work-around by declaring temp variable
            return Response(
                f"Uploaded {len(created_filenames)} files:\n{newline.join(created_filenames)}",
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            file = file_service.update_file(pk, request.data)
        except ConnectionError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        return Response(FileSerializer(file).data)

    def delete(self, request, pk):
        file_service.delete_file(pk)
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)
