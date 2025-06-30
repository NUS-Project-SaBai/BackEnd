from rest_framework.views import APIView
from rest_framework.response import Response
from random import randint

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition
from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, USE_MOCK_FACIAL_RECOGNITION

class PatientSearchView(APIView):

    def post(self, request):
        if ENABLE_FACIAL_RECOGNITION:
            face_encoding = facial_recognition.search_faceprint(request.data["picture"])
            ls = list(face_encoding.keys())
            patients = Patient.objects.filter(face_encodings__in=ls)
        elif USE_MOCK_FACIAL_RECOGNITION: # just select first 3 patients
            patients = Patient.objects.all()[0:3]
            face_encoding = {}
            for patient in patients:
                print(patient.name, ": ", patient.face_encodings)
                face_encoding[patient.face_encodings] = randint(1,99)/100
        else:
            return Response("Actual and mocked facial recognition are both not enabled", 503)
        serializer = PatientSerializer(
            patients, many=True, context={"confidence": face_encoding}
        )
        response = Response(serializer.data)
        if USE_MOCK_FACIAL_RECOGNITION:
            response.headers["x-is-mock-data"] = "True"
        return response
