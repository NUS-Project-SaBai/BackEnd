# api/views/file_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from api.services import file_service
from api.serializers import FileSerializer
from rest_framework import status


class FileView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return Response(file_service.get_file(pk))
        patient_pk = request.query_params.get("patient_pk", "")
        return Response(file_service.list_files(patient_pk))

    def post(self, request):
        try:
            uploaded_file = request.data.get("file")
            labeled_filename = request.data.get("file_name")
            patient_pk = request.data.get("patient_pk")
            file = file_service.create_file(uploaded_file, labeled_filename, patient_pk)
            return Response(FileSerializer(file).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        file = file_service.update_file(pk, request.data)
        return Response(FileSerializer(file).data)

    def delete(self, request, pk):
        file_service.delete_file(pk)
        return Response({"message": "Deleted successfully"})
