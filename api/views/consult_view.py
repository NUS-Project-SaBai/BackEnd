from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from api.serializers import *
from api.models import *
from rest_framework.response import Response


class ConsultView(APIView):
    def get(self, request):
        visit_key = request.query_params.get("visit")
        consults = Consult.objects.all() if visit_key is None else Consult.objects.filter(visit=visit_key)
        serializer = ConsultSerializer(consults, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        consult = Consult.objects.filter(pk=pk)
        serializer = ConsultSerializer(consult)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=500)

    def put(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        serializer = ConsultSerializer(consult, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=500)

    def delete(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        consult.delete()
        return Response({"message": "Deleted successfully"})