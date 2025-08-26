from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.patient_vision_service import get_patient_vision_viewmodel
from api.serializers.patient_vision_serializer import (
    PatientVisionOutputSerializer,
    VitalsVisionPickOut,
)


class PatientVisionView(APIView):
    def get(self, request):
        visit_id_raw = request.query_params.get("visit_id")
        try:
            visit_id = int(visit_id_raw or "0")
        except ValueError:
            return Response(
                {"detail": "visit_id must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if visit_id <= 0:
            return Response(
                {"detail": "visit_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        vm = get_patient_vision_viewmodel(visit_id)
        # payload = {
        #     "patient": PatientVisionVMOut.fields["patient"].to_representation(vm.patient),
        #     "vision": PatientVisionVMOut.fields["vision"].to_representation(vm.vision) if vm.vision else None,
        #     "vitals": VitalsVisionPickOut(vm.vitals).data if vm.vitals else None,
        # }
        patientVisionSerialized = PatientVisionOutputSerializer(vm)
        return Response(patientVisionSerialized.data, status=status.HTTP_200_OK)
