from django.urls import path
from api.views import UserView
from api.views.lock_user_view import LockUserView
from api.views.unlock_user_view import UnlockUserView

urlpatterns = [
    path("", UserView.as_view(), name="user_list"),
    path("<int:pk>/", UserView.as_view(), name="user_pk"),
    path("<str:username>/lock/", LockUserView.as_view(), name="user_lock"),
    path("<str:username>/unlock/", UnlockUserView.as_view(), name="user_unlock"),
]
