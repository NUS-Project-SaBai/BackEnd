from django.urls import path
from api.views import VitalsView

urlpatterns = [
    path("", VitalsView.as_view(), name="vitals_list"),
    path("<int:pk>/", VitalsView.as_view(), name="vitals_pk"),
]
