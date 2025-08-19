# api/views/file_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from api.services import file_service
from rest_framework import status


class FileView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return Response(file_service.get_file(pk), status=status.HTTP_200_OK)
        
        patient_pk = request.query_params.get("patient_pk", "")
        include_deleted = request.query_params.get("include_deleted", "").lower() in ("1", "true", "yes")
        return Response(file_service.list_files(patient_pk=patient_pk, include_deleted=include_deleted),
                        status=status.HTTP_200_OK,)

    def post(self, request):
        try:
            uploaded_file = request.FILES.get("offline_file") or request.FILES.get("file") or request.data.get("file")
            labeled_filename = request.data.get("file_name")
            patient_pk = request.data.get("patient_pk")

            description = request.data.get("description")
            data = file_service.create_file(uploaded_file, labeled_filename, patient_pk, description=description)
            return Response(data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        file = file_service.update_file(pk, request.data)
        return Response(file, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        data = file_service.delete_file(pk)
        return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)
