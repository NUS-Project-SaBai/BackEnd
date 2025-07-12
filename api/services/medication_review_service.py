from api.models import MedicationReview
from api.serializers import MedicationReviewSerializer


def list_medication_reviews(medication_pk=None):
    qs = MedicationReview.objects.all()
    if medication_pk:
        qs = qs.filter(medicine_id=medication_pk, order_status="APPROVED")
    return qs


def get_medication_review(pk):
    return MedicationReview.objects.filter(pk=pk).first()


def create_medication_review(data):
    serializer = MedicationReviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def update_medication_review(instance, data):
    serializer = MedicationReviewSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_medication_review(instance):
    instance.delete()
