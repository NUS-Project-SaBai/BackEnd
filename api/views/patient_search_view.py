from rest_framework.views import APIView 
from rest_framework.response import Response

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition

class PatientSearchView(APIView):

    def post(self, request):
        face_encoding = facial_recognition.search_faceprint(request.data['picture'])
        patients = Patient.objects.filter(face_encodings=face_encoding[0][0])
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
