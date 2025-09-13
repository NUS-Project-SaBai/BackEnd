from django.urls import path
from api.views import OrderView

urlpatterns = [
    path("", OrderView.as_view(), name="orders_list"),
    path("<int:pk>/", OrderView.as_view(), name="orders_pk"),
]
