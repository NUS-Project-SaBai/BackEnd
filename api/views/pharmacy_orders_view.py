# api/views/pharmacy_orders_view.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from api.services.pharmacy_orders_service import get_pharmacy_orders_viewmodel
from api.serializers.pharmacy_orders_serializer import PharmacyOrdersPatientSerializer

class PharmacyOrdersView(APIView):
    def get(self, request):
        vm_list = get_pharmacy_orders_viewmodel()
        return Response(PharmacyOrdersPatientSerializer(vm_list, many=True).data, status=200)
