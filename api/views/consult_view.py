from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Consult
from api.serializers import ConsultSerializer
from api import views
from django.db import transaction


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
        consult_data = request.data.get("consult")
        consult_data["doctor"] = views.utils.get_doctor_id(request.headers)
        consult_serializer = ConsultSerializer(data=consult_data)
        if consult_serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                consult = consult_serializer.save()
                orders_data = request.data.get("orders", [])
                diagnosis_data = request.data.get("diagnoses", [])
                for order_data in orders_data:
                    order_data["consult"] = consult.pk
                    views.OrderView.create(order_data)
                for data in diagnosis_data:
                    data["consult"] = consult.pk
                    views.DiagnosisView.create(data)
                return Response(consult_serializer.data)

    def patch(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        updated_consult_data = request.data.get("consult")
        # this updates the doctor id to the current doctor, not sure if intended??
        updated_consult_data["doctor"] = views.utils.get_doctor_id(
            request.headers)
        print(updated_consult_data)
        consult_serializer = ConsultSerializer(
            consult, data=request.data.get("consult"), partial=True)
        if consult_serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                consult_serializer.save()
                diagnosis_data = request.data.get("diagnoses", [])
                for data in diagnosis_data:
                    print(data)
                    data_filtered = {
                        "category": data.get("category"),
                        "details": data.get("details"),
                    }
                    views.DiagnosisView.update(
                        data_filtered, data.get("id"))
                return Response(consult_serializer.data)

    def delete(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        consult.delete()
        return Response({"message": "Deleted successfully"})
