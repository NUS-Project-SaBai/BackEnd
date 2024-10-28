from rest_framework.views import APIView 
from rest_framework.response import Response

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition

class PatientSearchView(APIView):

    def post(self, request):
        face_encoding = facial_recognition.search_faceprint(request.data['picture'])
        ls = list(face_encoding.keys())
        patients = Patient.objects.filter(face_encodings__in=ls)
        serializer = PatientSerializer(patients, many=True, context={'confidence':face_encoding})
        return Response(serializer.data)
