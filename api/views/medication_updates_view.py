from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import MedicationUpdates, Order
from api.serializers import MedicationUpdatesSerializer, OrderSerializer


class MedicationUpdatesView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        medication_updates = MedicationUpdates.objects.all()

        medication_pk = request.query_params.get("medication_pk", "")
        if medication_pk:
            medication_updates = medication_updates.filter(
                medicine_id=medication_pk,
                order_status='APPROVED'
            )

        orders = Order.objects.prefetch_related('medication_updates')

        medication_updates_data = []

        for medication_update in medication_updates:
            medication_update_data = MedicationUpdatesSerializer(
                medication_update).data
            order = orders.filter(medication_updates=medication_update).first()
            if order:
                order_data = OrderSerializer(order).data
                medication_update_data.update(order_data)
            else:
                medication_update_data['order'] = None

            medication_updates_data.append(medication_update_data)

        return Response(medication_updates_data)

    def get_object(self, pk):
        medication_history = MedicationUpdates.objects.filter(pk=pk).first()
        serializer = MedicationUpdatesSerializer(medication_history)
        return Response(serializer.data)

    def post(self, request):
        MedicationUpdatesView.new_entry(request.data)

    def patch(self, request, pk):
        medication_history = MedicationUpdates.objects.get(pk=pk)
        serializer = MedicationUpdatesSerializer(
            medication_history, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        medication_history = MedicationUpdates.objects.get(pk=pk)
        medication_history.delete()
        return Response({"message": "Deleted successfully"})

    @staticmethod
    def new_entry(data):
        print(data)
        serializer = MedicationUpdatesSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
