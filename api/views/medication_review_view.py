from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import MedicationReviewSerializer
from api.services import medication_review_service


class MedicationReviewView(APIView):
    def get(self, request, pk=None):
        if pk:
            review = medication_review_service.get_medication_review(pk)
            if not review:
                return Response({"error": "Not found"}, status=404)
            return Response(MedicationReviewSerializer(review).data)

        medication_pk = request.query_params.get("medication_pk")
        reviews = medication_review_service.list_medication_reviews(medication_pk)
        serializer = MedicationReviewSerializer(
            reviews, many=True, context={"include_order": True}
        )
        return Response(serializer.data)

    def post(self, request):
        review = medication_review_service.create_medication_review(request.data)
        return Response(
            MedicationReviewSerializer(review).data, status=status.HTTP_201_CREATED
        )

    def patch(self, request, pk):
        review = medication_review_service.get_medication_review(pk)
        if not review:
            return Response({"error": "Not found"}, status=404)
        updated = medication_review_service.update_medication_review(
            review, request.data
        )
        return Response(MedicationReviewSerializer(updated).data)

    def delete(self, request, pk):
        review = medication_review_service.get_medication_review(pk)
        if not review:
            return Response({"error": "Not found"}, status=404)
        medication_review_service.delete_medication_review(review)
        return Response(
            {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
