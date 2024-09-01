from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from api.models import Diagnosis
from api.serializers import DiagnosisSerializer


class DiagnosisView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        diagnoses = Diagnosis.objects.all()
        consult = request.query_params.get("consult", "")
        if consult:
            diagnoses = diagnoses.filter(consult=consult)
        serializer = DiagnosisSerializer(diagnoses, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        serializer = DiagnosisSerializer(diagnosis)
        return Response(serializer.data)

    def post(self, request):
        return DiagnosisView.create(request.data)

    def patch(self, request, pk):
        consult = Diagnosis.objects.get(pk=pk)
        serializer = DiagnosisSerializer(
            consult, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        diagnosis = Diagnosis.objects.get(pk=pk)
        diagnosis.delete()
        return Response({"message": "Deleted successfully"})

    @staticmethod
    def add(data):
        serializer = DiagnosisSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
