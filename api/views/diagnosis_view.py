from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import DiagnosisSerializer
from api.services import diagnosis_service


class DiagnosisView(APIView):
    def get(self, request, pk=None):
        if pk:
            diagnosis = diagnosis_service.get_diagnosis(pk)
            if not diagnosis:
                return Response(
                    {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = DiagnosisSerializer(diagnosis)
            return Response(serializer.data)

        consult_id = request.query_params.get("consult")
        diagnoses = diagnosis_service.list_diagnoses(consult_id)
        serializer = DiagnosisSerializer(diagnoses, many=True)
        return Response(serializer.data)

    def post(self, request):
        diagnosis = diagnosis_service.create_diagnosis(request.data)
        return Response(
            DiagnosisSerializer(diagnosis).data, status=status.HTTP_201_CREATED
        )

    def patch(self, request, pk):
        diagnosis = diagnosis_service.get_diagnosis(pk)
        if not diagnosis:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        updated_data = diagnosis_service.update_diagnosis(diagnosis, request.data)
        return Response(updated_data)

    def delete(self, request, pk):
        diagnosis = diagnosis_service.get_diagnosis(pk)
        if not diagnosis:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        diagnosis_service.delete_diagnosis(diagnosis)
        return Response(
            {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
