from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializers import MedicationSerializer
from api.services import medication_service
from api.utils.doctor_utils import get_doctor_id


class MedicationView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            meds = medication_service.list_medications()
            return Response(MedicationSerializer(meds, many=True).data)

        order_status = request.query_params.get("order_status")
        if order_status:
            data = medication_service.get_medication_with_pending(pk, order_status)
            return Response(data)

        med = medication_service.get_medication(pk)
        return Response(MedicationSerializer(med).data)

    def post(self, request):
        doctor_id = get_doctor_id(request.headers)
        med = medication_service.create_medication(request.data, doctor_id)
        return Response(MedicationSerializer(med).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        doctor_id = get_doctor_id(request.headers)
        data = medication_service.update_medication(pk, request.data, doctor_id)
        return Response(data)

    def delete(self, request, pk):
        med = medication_service.get_medication(pk)
        med.delete()
        return Response({"message": "Deleted successfully"})

    def update_quantity(self, quantityChange, pk):
        medication_service.update_quantity(pk, quantityChange)
