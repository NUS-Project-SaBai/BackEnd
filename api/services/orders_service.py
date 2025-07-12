from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from api.models import Order, MedicationReview, Medication, Diagnosis
from api.serializers import (
    OrderSerializer,
    MedicationReviewSerializer,
    DiagnosisSerializer,
)
from BackEnd.api.utils.doctor_utils import get_doctor_id

from collections import defaultdict


def get_order_by_id(pk):
    order = Order.objects.get(pk=pk)
    return OrderSerializer(order).data


def get_all_orders():
    return OrderSerializer(Order.objects.all(), many=True).data


def get_orders_with_embedded_diagnoses(order_status):
    # Step 1: Get all matching orders with related consults preloaded
    orders = Order.objects.filter(
        medication_review__order_status=order_status
    ).select_related("consult")

    # Step 2: Get all diagnoses for these consults
    consult_ids = {order.consult_id for order in orders if order.consult_id}
    diagnoses = Diagnosis.objects.filter(consult_id__in=consult_ids)

    # Step 3: Group diagnoses by consult_id
    diagnoses_by_consult = defaultdict(list)
    for diagnosis in diagnoses:
        diagnoses_by_consult[diagnosis.consult_id].append(
            DiagnosisSerializer(diagnosis).data
        )

    # Step 4: Attach diagnoses under each order
    result = []
    for order in orders:
        order_data = OrderSerializer(order).data
        order_data["diagnoses"] = diagnoses_by_consult.get(order.consult_id, [])
        result.append(order_data)

    return result


def create_order(order_data):
    quantity = int(order_data["quantity"])
    medicine = Medication.objects.get(pk=order_data["medicine"])
    medication_review_data = {
        "quantity_changed": -quantity,
        "quantity_remaining": medicine.quantity - quantity,
        "medicine": medicine,
        "order_status": "PENDING",
    }
    medication_review = MedicationReview.objects.create(**medication_review_data)

    order_data["medication_review"] = medication_review.pk
    serializer = OrderSerializer(data=order_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def update_order_status(order, request_data, request_headers):
    order_status = request_data.get("order_status")

    if order.medication_review.order_status in ["APPROVED", "CANCELLED"]:
        return Response(
            {"message": f"Order is already {order.medication_review.order_status}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if order_status == "PENDING":
        serializer = OrderSerializer(order, data=request_data, partial=True)
    elif order_status == "CANCELLED":
        serializer = MedicationReviewSerializer(
            order.medication_review, data=request_data, partial=True
        )
    elif order_status == "APPROVED":
        medicine = order.medication_review.medicine
        new_quantity = medicine.quantity + order.medication_review.quantity_changed

        if new_quantity < 0:
            return Response(
                {"error": "Medicine stock cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update medicine quantity directly
        medicine.quantity = new_quantity
        medicine.save()

        update_data = {
            "approval": get_doctor_id(request_headers),
            "quantity_remaining": new_quantity,
            "order_status": "APPROVED",
            "date": timezone.now(),
        }
        serializer = MedicationReviewSerializer(
            order.medication_review, data=update_data, partial=True
        )
    else:
        raise ValueError("Invalid order status")

    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
