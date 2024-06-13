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
        try:
            diagnosises = Diagnosis.objects.all()

            serializer = DiagnosisSerializer(diagnosises, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            diagnosis = Diagnosis.objects.filter(consult=pk)
            print(diagnosis)
            serializer = DiagnosisSerializer(diagnosis, many=True)
            return Response(serializer.data)    
        except Exception as e:
            return Response({"message": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = DiagnosisSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)})


    def put(self, request, pk):
        try:
            consult = Diagnosis.objects.get(pk=pk)
            serializer = DiagnosisSerializer(consult, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def delete(self, request, pk):
        try:
            diagnosis = Diagnosis.objects.get(pk=pk)
            diagnosis.delete()
            return Response({"message": "Deleted successfully"})
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)