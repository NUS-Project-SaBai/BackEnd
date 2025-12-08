from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ConsultSerializer
from api.services import consult_service
from datetime import timedelta, timezone
from datetime import datetime as dt


class ConsultView(APIView):
    def get(self, request, pk=None):
        if pk:
            consult = consult_service.get_consult(pk)
            if not consult:
                return Response({"error": "Not found"}, status=404)
            serializer = ConsultSerializer(consult)
            return Response(serializer.data)

        visit_key = request.query_params.get("visit")
        patient_ID = request.query_params.get("patientID")
        if visit_key:
            consults = consult_service.list_consults_by_visit_id(visit_key)
        elif patient_ID:
            consults = consult_service.list_consults_by_patient_id(patient_ID)

        serializer = ConsultSerializer(consults, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = consult_service.create_consult(request.data, request.headers)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        serializer = consult_service.update_consult_service(pk, request.data)
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        consult = consult_service.get_consult(pk)
        if not consult:
            return Response({"error": "Not found"}, status=404)
        consult.delete()
        return Response(
            {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
