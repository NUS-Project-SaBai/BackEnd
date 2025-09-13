from django.urls import path
from api.views.pharmacy_orders_view import PharmacyOrdersView

urlpatterns = [
    path("", PharmacyOrdersView.as_view(), name="pharmacy_orders"),
]
