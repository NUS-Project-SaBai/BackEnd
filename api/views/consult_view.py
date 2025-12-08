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
        consult = consult_service.get_consult(pk)
        if not consult:
            return Response({"error": "Not found"}, status=404)
        serializer = ConsultSerializer(consult, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Prevent editing if the consult was created more than 24 hours ago.
        if dt.now(timezone.utc) - consult.created_at > timedelta(hours=24):
            return Response({"error": "Cannot edit consult after 24 hours"}, status=405)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        consult = consult_service.get_consult(pk)
        if not consult:
            return Response({"error": "Not found"}, status=404)
        consult.delete()
        return Response(
            {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
