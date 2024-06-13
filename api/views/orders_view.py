from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Order
from api.serializers import OrderSerializer

class OrderView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        order_status = request.query_params.get('order_status', '')
        orders = Order.objects.all()
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        order = Order.objects.get(pk=pk)
        form = OrderSerializer(order, data=request.data, partial=True)
        if form.is_valid():
            form.save()
            return Response(form.data, content_type="application/json")
        return Response(form.errors, status=400)

    def delete(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"message": "Deleted successfully"})
