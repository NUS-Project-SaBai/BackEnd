from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Referrals
from api.serializers.referrals_serializer import ReferralSerializer
from rest_framework import status
from api.serializers.patient_serializer import PatientSerializer

class ReferralView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        response = []
        
        referrals = Referrals.objects.order_by("-pk")
        serializer_referral = ReferralSerializer(referrals, many=True) 

        for ref in serializer_referral.data:
            serializer_patient = PatientSerializer(self.get_patient_from_referral(ref["id"]))
            date = self.get_date_from_referral(ref["id"])
            response.append({
                "patient": serializer_patient.data,
                "referral": ref,
                "date": date
            })

        return Response(response)
    
    def patch(self, request, pk):

        referral = Referrals.objects.get(pk=pk)

        filtered_request_data = dict(
            filter(lambda item: item[1] != "", request.data.items())
        )
        
        serializer = ReferralSerializer(referral, data=filtered_request_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def get_object(self, pk):
        referral = Referrals.objects.get(pk=pk)
        serializer_referral = ReferralSerializer(referral)
        serializer_patient = PatientSerializer(self.get_patient_from_referral(pk))
        date = self.get_date_from_referral(pk)
        return Response({
            "patient": serializer_patient.data,
            "referral": serializer_referral.data,
            "date": date
        })
    
    def get_patient_from_referral(self, pk): #pk = referral ID
        referral = Referrals.objects.get(pk=pk)
        consult = referral.consult
        visit = consult.visit
        patient = visit.patient
        return patient
    
    def get_date_from_referral(self, pk):
        referral = Referrals.objects.get(pk=pk)
        consult = referral.consult
        return consult.date
    
    def post(self, request):
        serializer = ReferralSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)