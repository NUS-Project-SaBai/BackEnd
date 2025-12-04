from django.urls import path
from api.views.login_view import LoginView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
]
