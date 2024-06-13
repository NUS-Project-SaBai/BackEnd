from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from api.models import Diagnosis
from api.serializers import DiagnosisSerializer

class DiagnosisView(APIView):
    def get(self, request, pk=None):
        pk = request.query_params.get("consult")
        if pk is not None:
            return self.get_object(pk)
        diagnosises = Diagnosis.objects.all()

        serializer = DiagnosisSerializer(diagnosises, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        diagnosis = Diagnosis.objects.filter(consult=pk)
        print(diagnosis)
        serializer = DiagnosisSerializer(diagnosis, many=True)
        return Response(serializer.data)    

    def post(self, request):
        serializer = DiagnosisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


    def put(self, request, pk):
        consult = Diagnosis.objects.get(pk=pk)
        serializer = DiagnosisSerializer(consult, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        diagnosis.delete()
        return Response({"message": "Deleted successfully"})