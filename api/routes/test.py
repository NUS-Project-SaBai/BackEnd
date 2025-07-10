from django.urls import path
from api.views import TestView

urlpatterns = [
    path("", TestView.as_view(), name="test"),
]
