from rest_framework.views import APIView 
from rest_framework.response import Response

import base64

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition
from sabaibiometrics.custom_cache import photos_cache

class PatientSearchView(APIView):
    def get(self, request):
        # import pdb;pdb.set_trace()
        picture = photos_cache.get(request.user)
        base64_data = base64.b64encode(picture).decode('utf-8')
        print('cached picture:')
        print(type(base64_data))
        # return Response(picture)
        return Response(base64_data, content_type='application/octet-stream')

    def post(self, request):
        patient_data = request.data
        picture = patient_data.get("picture", None).file.getvalue()
        print('cached picture:')
        print(type(picture))
        photos_cache[request.user] = picture
        face_encoding = facial_recognition.search_faceprint(request.data['picture'])
        ls = list(face_encoding.keys())
        patients = Patient.objects.filter(face_encodings__in=ls)
        serializer = PatientSerializer(patients, many=True, context={'confidence':face_encoding})
        return Response(serializer.data)
