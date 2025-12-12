# api/services/referral_service.py
from api.models import Referrals
from api.serializers.referrals_serializer import ReferralSerializer
from api.serializers.patient_serializer import PatientSerializer
from api.serializers.user_serializer import UserSerializer

def get_referral(pk):
    return Referrals.objects.select_related("consult__doctor").get(pk=pk)


def get_referrals_by_consult(consult_id):
    return Referrals.objects.filter(consult__id=consult_id)


def list_referrals():
    return Referrals.objects.order_by("-pk")


def update_referral(instance, data):
    serializer = ReferralSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def create_referral(data):
    serializer = ReferralSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def serialize_patient_from_referral(referral):
    return PatientSerializer(referral.consult.visit.patient).data


def serialize_doctor_from_referral(referral):
    return UserSerializer(referral.consult.doctor).data


def get_date_from_referral(referral):
    return referral.consult.date
