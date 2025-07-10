from django.urls import path
from api.views import VisitView

urlpatterns = [
    path("", VisitView.as_view(), name="visits_list"),
    path("<int:pk>", VisitView.as_view(), name="visits_pk"),
]
