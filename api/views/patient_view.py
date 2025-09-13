from api.models.visit_model import Visit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, DateField, IntegerField

from api.models import Patient
from api.serializers import PatientSerializer
from api.services.patient_service import (
    extract_and_clean_picture,
    generate_face_encoding,
)

class PatientView(APIView):
    # get visits by patient id, ordered by date desc
    patient_visits_qs = Visit.objects.filter(patient_id=OuterRef('pk')).order_by('-date')
    # queryset of patient(s) annotated with their last visit date and id
    patients_with_last_visit_qs = Patient.objects.annotate(
            last_visit_date=Subquery(patient_visits_qs.values('date')[:1], output_field=DateField()),
            last_visit_id=Subquery(patient_visits_qs.values('pk')[:1], output_field=IntegerField()),
        )

    def get(self, request, pk=None):
        if pk:
            patient = get_object_or_404(self.patients_with_last_visit_qs, pk=pk)
            return Response(PatientSerializer(patient).data)
        
        patients = self.patients_with_last_visit_qs.order_by('-last_visit_date', '-pk')

        name = request.query_params.get("name")
        code = request.query_params.get("village_code")

        if name:
            patients = patients.filter(name__iexact=name)
        if code:
            patients = patients.filter(village_prefix__iexact=code)

        return Response(PatientSerializer(patients, many=True).data)

    def post(self, request):
        data = extract_and_clean_picture(request.data.copy())
        face_encoding = generate_face_encoding(data)

        serializer = PatientSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(face_encodings=face_encoding)
        return Response(serializer.data)

    def patch(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        data = extract_and_clean_picture(request.data.copy())

        serializer = PatientSerializer(patient, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()
        return Response({"message": "Deleted successfully"})
