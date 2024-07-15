from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Consult
from api.serializers import ConsultSerializer
from api.views.utils import get_doctor_id


class ConsultView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        consults = Consult.objects.all()
        visit_key = request.query_params.get("visit", "")
        if visit_key:
            consults = consults.filter(visit=visit_key)
        serializer = ConsultSerializer(consults, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        consult = Consult.objects.filter(pk=pk).first()
        serializer = ConsultSerializer(consult)
        return Response(serializer.data)

    def post(self, request):
        request.data["doctor"] = get_doctor_id(request)
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        serializer = ConsultSerializer(
            consult, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        consult.delete()
        return Response({"message": "Deleted successfully"})
