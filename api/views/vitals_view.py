from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import VitalsSerializer
from api.services import vitals_service
from api.models import Vitals


class VitalsView(APIView):
    def get(self, request, pk=None):
        if pk:
            vitals = vitals_service.get_vitals(pk)
            serializer = VitalsSerializer(vitals)
            return Response(serializer.data)

        visit_id = request.query_params.get("visit")
        vitals_qs = vitals_service.list_vitals(visit_id)
        serializer = VitalsSerializer(vitals_qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VitalsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vitals = serializer.save()
        return Response(VitalsSerializer(vitals).data)

    def patch(self, request, pk=None):
        if pk:
            vital = vitals_service.get_vitals(pk)
        else:
            visit_id = request.query_params.get("visit")
            vital = vitals_service.list_vitals(visit_id).first()

        serializer = VitalsSerializer(vital, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_vital = serializer.save()
        return Response(VitalsSerializer(updated_vital).data)

    def delete(self, request, pk):
        vitals_service.delete_vitals(pk)
        return Response({"message": "Deleted successfully"})
