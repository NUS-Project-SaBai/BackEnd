from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from api.models import Order, MedicationUpdates, Medication
from api.serializers import OrderSerializer, MedicationUpdatesSerializer
from api.views import MedicationView
from datetime import datetime
from api.views.utils import get_doctor_id


class OrderView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        orders = Order.objects.all()
        order_status = request.query_params.get("order_status", "")
        if order_status:
            orders = orders.filter(
                medication_updates__order_status=order_status)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request):
        order_data = request.data
        print(order_data)
        # order_data["medication_update"] = {
        #     "approval": get_doctor_id(request.headers),
        #     "quantity_change": -order_data["quantity"],
        #     "quantity_remaining": order_data["medicine"].quantity - order_data["quantity"],
        #     "medicine": order_data["medicine"].pk,
        #     "order_status": "PENDING",
        # }
        # order_data["doctor"] = get_doctor_id(request.headers)
        quantity = int(order_data['quantity'])
        medicine = Medication.objects.get(pk=order_data['medicine'])
        print(medicine)
        medication_update_data = {
            "quantity_changed": -quantity,
            "quantity_remaining": medicine.quantity - quantity,
            "medicine": medicine,
            "order_status": "PENDING",
        }
        medication_update = MedicationUpdates.objects.create(
            **medication_update_data)
        order_data['medication_updates'] = medication_update.pk
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # WARNING not updating orders
    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        if order.medication_updates.order_status == "APPROVED" or order.medication_updates.order_status == "CANCELLED":
            return Response({f"message": "Order already is already {order.medication_updates.order_status}"})
        order_status = request.data.get("order_status")

        if order_status == "PENDING":
            serializer = OrderSerializer(
                order, data=request.data, partial=True)
        elif order_status == "CANCELLED":
            serializer = MedicationUpdatesSerializer(
                order.medication_updates, data=request.data, partial=True)
        else:
            medication_update_data = {
                "approval": get_doctor_id(request.headers),
                "quantity_remaining": order.medication_updates.medicine.quantity + order.medication_updates.quantity_changed,
                "order_status": order_status,
                "date": datetime.now(),
            }
            serializer = MedicationUpdatesSerializer(
                order.medication_updates, data=medication_update_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                if order_status == "APPROVED":
                    MedicationView().update_quantity(quantityChange=order.medication_updates.quantity_changed,
                                                     pk=order.medication_updates.medicine.pk)
                serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"message": "Deleted successfully"})
