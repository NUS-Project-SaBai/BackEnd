from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Visit
from api.serializers import VisitSerializer


class VisitView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        visits = Visit.objects.all()
        patient = request.query_params.get("patient", "")
        if patient:
            visits = (
                visits.select_related("patient")
                .filter(patient_id=patient)
                .order_by("-id")
            )
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        visit = Visit.objects.get(pk=pk)
        serializer = VisitSerializer(visit)
        return Response(serializer.data)

    def post(self, request):
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        serializer = VisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        visit = Visit.objects.get(pk=pk)
        visit.delete()
        return Response({"message": "Deleted successfully"})
