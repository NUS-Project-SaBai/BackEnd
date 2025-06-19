from api.models.visit_model import Visit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, DateTimeField, Value
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone

from api.models import Patient
from api.serializers import PatientSerializer
from api.utils import facial_recognition

from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION, OFFLINE


class PatientView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        # # Check if any visits exist for a test patient
        # test_patient = Patient.objects.first()
        # print("check:")
        # print(Visit.objects.filter(patient=test_patient).exists())  # Should return True/False

        # # Get the latest visit date for each patient
        # latest_visit_subquery = Visit.objects.filter(
        #     patient_id=OuterRef('pk')
        # ).order_by('-date').values('date')[:1]

        # patients = Patient.objects.annotate(
        #     last_visit=Subquery(latest_visit_subquery)
        # ).order_by("-last_visit").order_by("-pk")

        patients = Patient.objects.annotate(
            last_visit=Subquery(
                Visit.objects.filter(patient_id=OuterRef('pk'))
                .order_by('-date')
                .values('date')
            )
        ).order_by("-last_visit", "-pk")

        # Check if visits exist for first patient
        test_patient = Patient.objects.first()
        visits = Visit.objects.filter(patient=test_patient).order_by('-date')
        print(visits.exists())  # Should be True
        print(visits.first().date)  # Should show a valid datetime

        test_subquery = Visit.objects.filter(patient_id=1).order_by('-date').values('date')[:1]
        print(Subquery(test_subquery))  # Should return a date

        patients = Patient.objects.annotate(
            last_visit=Subquery(
                Visit.objects.filter(patient_id=OuterRef('pk'))
                .order_by('-date')
                .values('date')#[:1]  # Critical: must limit to 1 row
                # Explicitly cast if needed:
                # .annotate(date_as_dt=Cast('date', DateTimeField()))
                # .values('date_as_dt')[:1]
            )
        ).order_by("-pk")

        patients = Patient.objects.annotate(
            # TEST 1: Hardcoded value
            last_visit_test=Value("2023-01-01"),  # Static string
            
            # TEST 2: Current time (dynamic)
            last_visit_now=Value(timezone.now()),
            
            # TEST 3: Subquery with Coalesce as fallback
            last_visit_real=Coalesce(
                Subquery(
                    Visit.objects.filter(patient_id=OuterRef('pk'))
                    .order_by('-date')
                    .values('date')[:1]
                ),
                Value("NO_VISITS")  # Fallback value
            )
        ).order_by("-pk")

        patient_name = request.query_params.get("name", "")
        patient_village_code = request.query_params.get("village_code", "")
        if patient_name:
            patients = patients.filter(name__iexact=patient_name)
        if patient_village_code:
            patients = patients.filter(village_prefix__iexact=patient_village_code)
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
