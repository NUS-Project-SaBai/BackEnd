from django.urls import path
from api.views import PatientView, PatientSearchView

urlpatterns = [
    path("", PatientView.as_view(), name="patients_list"),
    path("<int:pk>/", PatientView.as_view(), name="patients_pk"),
    path("search_face/", PatientSearchView.as_view(), name="patients_list"),
]
