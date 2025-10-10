from django.urls import path
from api.views import DiagnosisView

urlpatterns = [
    path("", DiagnosisView.as_view(), name="diagnosis_list"),
    path("<int:pk>/", DiagnosisView.as_view(), name="diagnosis_pk"),
]
