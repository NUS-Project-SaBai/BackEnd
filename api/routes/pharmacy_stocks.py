from django.urls import path
from api.views.pharmacy_stocks_view import MedicationHistoryView

urlpatterns = [
    path("", MedicationHistoryView.as_view(), name="pharmacy_stocks"),
]
