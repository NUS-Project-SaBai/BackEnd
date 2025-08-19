# In pharmacy_stocks_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.pharmacy_stocks_service import get_pharmacy_stock_viewmodel
from api.serializers.pharmacy_stocks_serializer import PharmacyStockSerializer

class PharmacyStocksView(APIView):
    def get(self, request):
        pharmacy_stocks = get_pharmacy_stock_viewmodel()
        pharmacy_stocks_serialized = PharmacyStockSerializer(pharmacy_stocks, many=True)
        return Response(pharmacy_stocks_serialized.data)
