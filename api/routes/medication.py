from django.urls import path
from api.views import MedicationView

urlpatterns = [
    path("", MedicationView.as_view(), name="medications_list"),
    path("<int:pk>", MedicationView.as_view(), name="medications_pk"),
]
