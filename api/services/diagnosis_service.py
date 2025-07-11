from api.models import Diagnosis
from api.serializers import DiagnosisSerializer
from rest_framework.response import Response


def list_diagnoses(consult_id=None):
    qs = Diagnosis.objects.all()
    if consult_id:
        qs = qs.filter(consult=consult_id)
    return qs


def get_diagnosis(pk):
    return Diagnosis.objects.filter(pk=pk).first()


def create_diagnosis(data):
    serializer = DiagnosisSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def update_diagnosis(instance, data):
    serializer = DiagnosisSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data


def delete_diagnosis(instance):
    instance.delete()
