from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import File
from api.serializers import FileSerializer
import os
import tempfile
from api.views import utils
from sabaibiometrics.settings import OFFLINE


class FileView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        files = File.objects.all()

        patient_pk = request.query_params.get("patient_pk", "")
        if patient_pk:
            files = files.filter(
                patient_id=patient_pk
            )

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        users = File.objects.get(pk=pk)
        serializer = FileSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        uploaded_file = request.data.get('file')
        labeled_filename = request.data.get('file_name')
        patient_pk = request.data.get('patient_pk')

        if not uploaded_file:
            return Response({'error': 'No file was uploaded'}, status=400)

        if not labeled_filename:
            return Response({'error': 'No labeled filename provided'}, status=400)

        data = {
            "patient": patient_pk,
            "file_name": labeled_filename
        }

        if OFFLINE:
            data["offline_file"] = uploaded_file
        else:
            data["file_path"] = utils.upload_photo(
                uploaded_file, labeled_filename)

        serializer = FileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        user = File.objects.get(pk=pk)
        serializer = FileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        user = File.objects.get(pk=pk)
        user.delete()
        return Response({"message": "Deleted successfully"})
