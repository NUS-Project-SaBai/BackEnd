from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path("medications", views.MedicationView.as_view()),
    path("medications/<int:pk>", views.MedicationView.as_view()),
    path("user", views.UserView.as_view()),
    path("user/<int:pk>", views.UserView.as_view()),
    path("consult", views.ConsultView.as_view()),
    path("consult/<int:pk>", views.ConsultView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
