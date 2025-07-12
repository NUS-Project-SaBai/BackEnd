from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import PatientSerializer
from api.services import patient_service


class PatientSearchView(APIView):
    def post(self, request):
        picture = request.data["picture"]
        patients, confidence_dict = patient_service.search_patients_by_face(picture)
        serializer = PatientSerializer(
            patients,
            many=True,
            context={"confidence": confidence_dict},
        )
        return Response(serializer.data)
