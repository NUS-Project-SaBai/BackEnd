from api.models import Glasses, Visit
from django.shortcuts import get_object_or_404


def get_glasses_by_visit(visit_id):
    return Glasses.objects.filter(visit_id=visit_id).order_by("-id").first()


def get_all_glasses():
    return Glasses.objects.all()


def get_glasses(pk):
    return get_object_or_404(Glasses, pk=pk)


def create_glasses(validated_data, visit):
    return Glasses.objects.create(visit=visit, **validated_data)


def update_glasses(instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance
