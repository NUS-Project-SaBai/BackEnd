from api.models import Visit
from django.shortcuts import get_object_or_404


def list_visits(patient_id=None):
    visits = Visit.objects.all().select_related("patient")
    if patient_id:
        visits = visits.filter(patient_id=patient_id).order_by("-id")
    return visits


def get_visit(pk):
    return get_object_or_404(Visit, pk=pk)


def create_visit(validated_data):
    return Visit.objects.create(**validated_data)


def update_visit(instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance


def delete_visit(instance):
    instance.delete()
