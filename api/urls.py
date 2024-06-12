from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path("medications", views.MedicationView.as_view()),
    path("medications/<int:pk>", views.MedicationView.as_view()),
    path("patients", views.PatientView.as_view(), name="patients"),
    path("patients/<int:pk>", views.PatientView.as_view(), name="patients_detail"),
    path("orders", views.OrderView.as_view()),
    path("orders/<int:pk>", views.OrderView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
