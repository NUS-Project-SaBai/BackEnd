from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import VisitSerializer
from api.services import visit_service


class VisitView(APIView):
    def get(self, request, pk=None):
        if pk:
            visit = visit_service.get_visit(pk)
            serializer = VisitSerializer(visit)
            return Response(serializer.data)

        patient_id = request.query_params.get("patient")
        visits = visit_service.list_visits(patient_id)
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    def post(self, request):
        visit_serializer: VisitSerializer = visit_service.create_visit(
            data=request.data
        )
        return Response(visit_serializer.data)

    def patch(self, request, pk):
        visit = visit_service.get_visit(pk)
        serializer = VisitSerializer(visit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_visit = visit_service.update_visit(visit, serializer.validated_data)
        return Response(VisitSerializer(updated_visit).data)

    def delete(self, request, pk):
        visit = visit_service.get_visit(pk)
        visit_service.delete_visit(visit)
        return Response({"message": "Deleted successfully"})
