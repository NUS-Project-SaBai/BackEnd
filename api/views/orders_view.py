from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from api.models import Order, MedicationReview, Medication
from api.serializers import OrderSerializer, MedicationReviewSerializer
from api.views import MedicationView
from django.utils import timezone
from api.views.utils.utils import get_doctor_id


class OrderView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        orders = Order.objects.all()
        order_status = request.query_params.get("order_status", "")
        if order_status:
            orders = orders.filter(
                medication_review__order_status=order_status)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request):
        return OrderView.add(request.data)

    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        if (
            order.medication_review.order_status == "APPROVED"
            or order.medication_review.order_status == "CANCELLED"
        ):
            return Response(
                {
                    f"message": "Order already is already {order.medication_review.order_status}"
                }
            )
        order_status = request.data.get("order_status")

        if order_status == "PENDING":
            serializer = OrderSerializer(
                order, data=request.data, partial=True)
        elif order_status == "CANCELLED":
            serializer = MedicationReviewSerializer(
                order.medication_review, data=request.data, partial=True
            )
        elif order_status == "APPROVED":
            medication_review_data = {
                "approval": get_doctor_id(request.headers),
                "quantity_remaining": order.medication_review.medicine.quantity
                + order.medication_review.quantity_changed,
                "order_status": order_status,
                "date": timezone.now(),
            }
            serializer = MedicationReviewSerializer(
                order.medication_review, data=medication_review_data, partial=True
            )
        else:
            raise ValueError("Invalid order status")

        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                if order_status == "APPROVED":
                    MedicationView().update_quantity(
                        quantityChange=order.medication_review.quantity_changed,
                        pk=order.medication_review.medicine.pk,
                    )
                serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"message": "Deleted successfully"})

    @staticmethod
    def add(order_data):
        quantity = int(order_data["quantity"])
        medicine = Medication.objects.get(pk=order_data["medicine"])
        medication_review_data = {
            "quantity_changed": -quantity,
            "quantity_remaining": medicine.quantity - quantity,
            "medicine": medicine,
            "order_status": "PENDING",
        }
        medication_review = MedicationReview.objects.create(
            **medication_review_data)
        order_data["medication_review"] = medication_review.pk
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
