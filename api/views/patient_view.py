from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition

from sabaibiometrics.settings import OFFLINE


class PatientView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        patients = Patient.objects.order_by("-pk").all()
        patient_name = request.query_params.get("name", "")
        if patient_name:
            patients = Patient.objects.filter(name=patient_name)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def post(self, request):
<<<<<<< HEAD
        patient_data = request.data
        if OFFLINE:
            offline_picture = patient_data.pop("picture", None)
            patient_data["offline_picture"] = offline_picture
        serializer = PatientSerializer(data=patient_data)
        face_encoding = facial_recognition.generate_faceprint(patient_data['picture']) if not OFFLINE else ''
=======
        serializer = PatientSerializer(data=request.data)
        print(f"picture type: {type(request.data['picture'])} to string: {str(request.data['picture'])}")
        face_encoding = facial_recognition.generate_faceprint(request.FILES['picture'])
>>>>>>> 1458a84 (Merge tests)
        if serializer.is_valid(raise_exception=True):
            serializer.save(face_encodings=face_encoding)
            return Response(serializer.data)

    def patch(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        serializer = PatientSerializer(
            patient, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})