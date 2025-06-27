from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Consult
from api.serializers import ConsultSerializer
from api import views
from django.db import transaction
from api.views import utils


class ConsultView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        consults = Consult.objects.all()

        visit_key = request.query_params.get("visit", "")
        patient_ID = request.query_params.get("patientID", "")    

        if visit_key:
            consults = consults.filter(visit=visit_key)
        elif patient_ID:
            consults = consults.filter(visit__patient__pk=patient_ID)

        serializer = ConsultSerializer(consults, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        consult = Consult.objects.filter(pk=pk).first()
        serializer = ConsultSerializer(consult)
        return Response(serializer.data)

    def post(self, request):
        consult_data = request.data.get("consult")
        consult_data["doctor"] = utils.get_doctor_id(request.headers)
        consult_serializer = ConsultSerializer(data=consult_data)

        if consult_serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                consult = consult_serializer.save()
                orders_data = request.data.get("orders", [])
                diagnosis_data = request.data.get("diagnoses", [])
                for order_data in orders_data:
                    order_data["consult"] = consult.pk
                    views.OrderView.add(order_data)
                for diagnosis_data in diagnosis_data:
                    diagnosis_data["consult"] = consult.pk
                    views.DiagnosisView.add(diagnosis_data)
                return Response(consult_serializer.data)

    def patch(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        serializer = ConsultSerializer(consult, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        consult.delete()
        return Response({"message": "Deleted successfully"})
