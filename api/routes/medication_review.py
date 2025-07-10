from django.urls import path
from api.views import MedicationReviewView

urlpatterns = [
    path("", MedicationReviewView.as_view(), name="medication_review_list"),
    path("<int:pk>", MedicationReviewView.as_view(), name="medication_review_pk"),
]
