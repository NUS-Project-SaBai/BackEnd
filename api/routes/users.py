from django.urls import path
from api.views import UserView

urlpatterns = [
    path("", UserView.as_view(), name="user_list"),
    path("<int:pk>/", UserView.as_view(), name="user_pk"),
]
