from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services import referral_service


class ReferralView(APIView):
    def get(self, request, pk=None):
        if pk:
            return self.get_object(pk)

        referrals = referral_service.list_referrals()
        response = []
        for ref in referrals:
            patient_data = referral_service.serialize_patient_from_referral(ref)
            date = referral_service.get_date_from_referral(ref)
            response.append(
                {
                    "patient": patient_data,
                    "referral": referral_service.ReferralSerializer(ref).data,
                    "date": date,
                }
            )

        return Response(response)

    def get_object(self, pk):
        ref = referral_service.get_referral(pk)
        return Response(
            {
                "patient": referral_service.serialize_patient_from_referral(ref),
                "referral": referral_service.ReferralSerializer(ref).data,
                "date": referral_service.get_date_from_referral(ref),
            }
        )

    def patch(self, request, pk):
        referral = referral_service.get_referral(pk)
        filtered_data = {k: v for k, v in request.data.items() if v != ""}
        updated = referral_service.update_referral(referral, filtered_data)
        return Response(referral_service.ReferralSerializer(updated).data)

    def post(self, request):
        referral = referral_service.create_referral(request.data)
        return Response(
            referral_service.ReferralSerializer(referral).data,
            status=status.HTTP_201_CREATED,
        )
