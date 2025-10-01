from rest_framework.views import APIView
from rest_framework.response import Response
from random import randint
from django.db.models import OuterRef, Subquery, DateField, IntegerField

from api.models import Patient
from api.models.visit_model import Visit
from api.serializers import PatientSerializer
from api.services import patient_service
from sabaibiometrics.settings import (
    ENABLE_FACIAL_RECOGNITION,
    USE_MOCK_FACIAL_RECOGNITION,
)


class PatientSearchView(APIView):
    patient_visits_qs = Visit.objects.filter(patient_id=OuterRef('pk')).order_by('-date')
    
    def post(self, request):
        if ENABLE_FACIAL_RECOGNITION:
            picture = request.data["picture"]
            patients, confidence_dict = patient_service.search_patients_by_face(picture)
        elif USE_MOCK_FACIAL_RECOGNITION:  # just select first 3 patients
            patients = Patient.objects.all()[0:3]
            confidence_dict = {}
            for patient in patients:
                confidence_dict[patient.face_encodings] = randint(1, 99) / 100
        else:
            return Response(
                "Actual and mocked facial recognition are both not enabled", 503
            )

        patients = patients.annotate(
            last_visit_date=Subquery(self.patient_visits_qs.values('date')[:1], output_field=DateField()),
            last_visit_id=Subquery(self.patient_visits_qs.values('pk')[:1], output_field=IntegerField()),
        )

        serializer = PatientSerializer(
            patients, many=True, context={"confidence": confidence_dict}
        )
        response = Response(serializer.data)
        if USE_MOCK_FACIAL_RECOGNITION:
            response.headers["x-is-mock-data"] = "True"
        return response
