from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path("test", views.TestView.as_view(), name="test"),
    path("medications", views.MedicationView.as_view(), name="medications_list"),
    path(
        "medications/<int:pk>",
        views.MedicationView.as_view(),
        name="medications_detail",
    ),
    path("patients", views.PatientView.as_view(), name="patients_list"),
    path("patients/<int:pk>", views.PatientView.as_view(), name="patients_detail"),
    path("visits", views.VisitView.as_view(), name="visits_list"),
    path("visits/<int:pk>", views.VisitView.as_view(), name="visits_detail"),
    path("vitals", views.VitalsView.as_view(), name="vitals_list"),
    path("vitals/<int:pk>", views.VitalsView.as_view(), name="vitals_detail"),
    path("user", views.UserView.as_view(), name="user_list"),
    path("user/<int:pk>", views.UserView.as_view(), name="user_detail"),
    path("consults", views.ConsultView.as_view(), name="consults_list"),
    path("consults/<int:pk>", views.ConsultView.as_view(), name="consults_detail"),
    path("diagnosis", views.DiagnosisView.as_view(), name="diagnosis_list"),
    path("diagnosis/<int:pk>", views.DiagnosisView.as_view(),
         name="diagnosis_detail"),
    path("orders", views.OrderView.as_view(), name="orders_list"),
    path("orders/<int:pk>", views.OrderView.as_view(), name="orders_detail"),
    path("medication_review", views.MedicationReviewView.as_view(),
         name="medication_review_list"),
    path("medication_review/<int:pk>", views.MedicationReviewView.as_view(),
         name="medication_review_detail"),
    path('upload/', views.upload_file, name='upload_file'),
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
