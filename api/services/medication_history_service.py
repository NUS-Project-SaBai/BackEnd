from api.viewmodels.medication_history_viewmodel import MedicationHistoryViewModel
from api.models import MedicationReview, Order


# returns a list of medication history view models
def get_medication_history_viewmodel(medicine_id: int):
    medication_reviews = MedicationReview.objects.filter(
        medicine_id=medicine_id
    ).order_by("-date")

    medication_history_list = []

    for review in medication_reviews:
        order = Order.objects.filter(medication_review=review).first()
        consult = order.consult if order else None

        medication_history_list.append(MedicationHistoryViewModel(review, consult))
    return medication_history_list
