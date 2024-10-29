from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Patient
from api.serializers import PatientSerializer

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
        # for django request.data returns a MultiQuery Object.
        # MultiQuery will wrap all the data value into a list
        patient_data = request.data
        if OFFLINE:
            # IMPT: pop and get to be done separately!
            # next line just returns the data value without the list
            offline_picture = patient_data.get("picture", None)
            # next line is just to delete it
            patient_data.pop("picture")
            patient_data["offline_picture"] = offline_picture
        serializer = PatientSerializer(data=patient_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        patient_data = request.data
        if OFFLINE:
            offline_picture = patient_data.get("picture", None)
            patient_data.pop("picture")
            patient_data["offline_picture"] = offline_picture
        serializer = PatientSerializer(patient, data=patient_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        patient = Patient.objects.get(pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})
