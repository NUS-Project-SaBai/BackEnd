from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from api.models import Order
from api.serializers import OrderSerializer
from api.views import MedicationView, MedicationHistoryView


class OrderView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        orders = Order.objects.all()
        order_status = request.query_params.get("order_status", "")
        if order_status:
            orders = orders.filter(order_status=order_status)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        order_status = request.data.get("order_status")
        form = OrderSerializer(order, data=request.data, partial=True)
        if form.is_valid(raise_exception=True):
            with transaction.atomic():
                form.save()
                if order_status == "APPROVED":
                    MedicationView().update_quantity(
                        quantityChange=-order.quantity, pk=order.medicine.pk)

                medication_history_data = {
                    "doctor": order.consult.doctor.auth0_id,
                    "patient": order.consult.visit.patient.pk,
                    "quantity_changed": -order.quantity,
                    "quantity_remaining": order.medicine.quantity - order.quantity,
                    "medicine": order.medicine.pk,
                }
                MedicationHistoryView.new_entry(medication_history_data)
            return Response(form.data)

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"message": "Deleted successfully"})
