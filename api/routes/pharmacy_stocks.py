from django.urls import path
from api.views.pharmacy_stocks_view import PharmacyStocksView

urlpatterns = [
    path("", PharmacyStocksView.as_view(), name="pharmacy_stocks"),
]
