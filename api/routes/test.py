from django.urls import path
from api.views import HelloView

urlpatterns = [
    path("", HelloView.as_view(), name="test"),
]
