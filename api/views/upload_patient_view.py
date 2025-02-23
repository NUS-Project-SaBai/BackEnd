from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Patient
from api.serializers import PatientSerializer

class UploadPatientView(APIView):

    def post(self, request):
        serializer = PatientSerializer(data=request.data, many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)