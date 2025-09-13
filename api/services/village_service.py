from api.models import Village
from django.shortcuts import get_object_or_404


# filter out deleted villages
def get_all_villages():
    return Village.objects.filter(is_hidden=False)


def get_village_by_id(pk):
    return get_object_or_404(Village, pk=pk)


def create_village(validated_data):
    return Village.objects.create(**validated_data)


def edit_village(instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance
