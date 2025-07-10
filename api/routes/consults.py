from django.urls import path
from api.views import ConsultView

urlpatterns = [
    path("", ConsultView.as_view(), name="consults_list"),
    path("<int:pk>", ConsultView.as_view(), name="consults_pk"),
]
