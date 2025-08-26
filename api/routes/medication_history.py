from django.urls import path
from api.views.medication_history_view import MedicationHistoryView

urlpatterns = [
    path("", MedicationHistoryView.as_view(), name="medication_history"),
]
