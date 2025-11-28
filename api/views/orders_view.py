from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Order, Diagnosis
from api.serializers import OrderSerializer, DiagnosisSerializer
from api.services import orders_service


class OrderView(APIView):
    def get(self, request, pk=None):
        if pk:
            data = orders_service.get_order_by_id(pk)
            return Response(data, status=status.HTTP_200_OK)

        order_status = request.query_params.get("order_status", "").upper()
        if order_status:
            data = orders_service.get_orders_with_embedded_diagnoses(order_status)
            return Response(data, status=status.HTTP_200_OK)

        data = orders_service.get_all_orders()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        order = orders_service.create_order(request.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        return orders_service.update_order_status(order, request.data, request.headers)

    def delete(self, request, pk):
        Order.objects.get(pk=pk).delete()
        return Response({"message": "Deleted successfully"})
