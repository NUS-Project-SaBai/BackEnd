from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch

from api.models import MedicationReview, Order
from api.serializers import MedicationReviewSerializer


class MedicationReviewView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        medication_reviews = MedicationReview.objects.all()

        medication_pk = request.query_params.get("medication_pk", "")
        if medication_pk:
            medication_reviews = medication_reviews.filter(
                medicine_id=medication_pk,
                order_status='APPROVED'
            )

        medication_reviews.prefetch_related(
            Prefetch('order', queryset=Order.objects.all())
        )
        return Response(MedicationReviewSerializer(medication_reviews, many=True).data)

    def get_object(self, pk):
        medication_history = MedicationReview.objects.filter(pk=pk).first()
        serializer = MedicationReviewSerializer(medication_history)
        return Response(serializer.data)

    def post(self, request):
        MedicationReviewSerializer.new_entry(request.data)

    def patch(self, request, pk):
        medication_history = MedicationReview.objects.get(pk=pk)
        serializer = MedicationReviewSerializer(
            medication_history, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        medication_history = MedicationReview.objects.get(pk=pk)
        medication_history.delete()
        return Response({"message": "Deleted successfully"})

    @staticmethod
    def new_entry(data):
        print(data)
        serializer = MedicationReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
