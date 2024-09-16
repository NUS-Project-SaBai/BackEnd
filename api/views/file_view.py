from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import File
from api.serializers import FileSerializer
import os
import tempfile
from api.views import utils


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

        file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)

        # Save the file temporarily
        with open(file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Call the function to upload to Google Drive
        file_url = utils.upload_photo(file_path, labeled_filename)

        # Optionally delete the temp file
        os.remove(file_path)

        data = {
            "patient": patient_pk,
            "file_path": file_url,
            "file_name": labeled_filename
        }

        serializer = FileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        # serializer = FileSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        #     return Response(serializer.data)

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
