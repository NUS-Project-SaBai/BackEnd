from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path("medications", views.MedicationView.as_view()),
    path("medications/<int:pk>", views.MedicationView.as_view()),
    path("patients", views.PatientView.as_view()),
    path("patients/<int:pk>", views.PatientView.as_view()),
    path("visits", views.VisitView.as_view()),
    path("visits/<int:pk>", views.VisitView.as_view()),
    path("vitals", views.VitalsView.as_view()),
    path("vitals/<int:pk>", views.VitalsView.as_view()),
    path("user", views.UserView.as_view()),
    path("user/<int:pk>", views.UserView.as_view()),
    path("consults", views.ConsultView.as_view()),
    path("consults/<int:pk>", views.ConsultView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
