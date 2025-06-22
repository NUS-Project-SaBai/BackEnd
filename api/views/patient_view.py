from api.models.visit_model import Visit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, DateField, IntegerField

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition

from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, OFFLINE

# last_visit_subquery = Subquery(
#     Visit.objects.filter(patient_id=OuterRef('pk'))
#     .order_by('-date')
#     .values('date')[:1]
# )

last_visit_qs = Visit.objects.filter(patient_id=OuterRef('pk')).order_by('-date')

class PatientView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        # patients = Patient.objects.annotate(
        #     last_visit=last_visit_subquery
        # ).order_by("-last_visit", "-pk")

        patients = Patient.objects.annotate(
            last_visit_date=Subquery(last_visit_qs.values('date')[:1], output_field=DateField()),
            last_visit_id=Subquery(last_visit_qs.values('pk')[:1], output_field=IntegerField()),
        ).order_by('-last_visit_date', '-pk')

        patient_name = request.query_params.get("name", "")
        patient_village_code = request.query_params.get("village_code", "")
        if patient_name:
            patients = patients.filter(name__iexact=patient_name)
        if patient_village_code:
            patients = patients.filter(village_prefix__iexact=patient_village_code)
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        patient = Patient.objects.annotate(
            last_visit_date=Subquery(last_visit_qs.values('date')[:1], output_field=DateField()),
            last_visit_id=Subquery(last_visit_qs.values('pk')[:1], output_field=IntegerField()),
        ).get(pk=pk)
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
        # print("ok")
        if OFFLINE:
            face_encoding = (
                facial_recognition.generate_faceprint(patient_data["offline_picture"])
                if ENABLE_FACIAL_RECOGNITION
                else ""
            )
        else:
            face_encoding = (
                facial_recognition.generate_faceprint(patient_data["picture"])
                if ENABLE_FACIAL_RECOGNITION
                else ""
            )
        # print(face_encoding)
        if serializer.is_valid(raise_exception=True):
            serializer.save(face_encodings=face_encoding)
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
