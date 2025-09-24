from api.models import Village
from django.shortcuts import get_object_or_404


# filter out deleted villages
def get_all_villages(is_hidden=False):
    """Retrieve all Villages filtered by their 'is_hidden' status.

    Parameters
    ----------
        is_hidden : bool, optional
            The visibility status of villages to retrieve. Defaults to False.
            - If True, retrieves villages marked as hidden (deleted).
            - If False, retrieves only visible villages.
            - If None, retrieves all villages regardless of their hidden status.
    """
    if is_hidden is None:
        return Village.objects.all()
    return Village.objects.filter(is_hidden=is_hidden)


def get_village_by_id(pk):
    return get_object_or_404(Village, pk=pk)


def create_village(validated_data):
    return Village.objects.create(**validated_data)


def edit_village(instance, validated_data):
    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()
    return instance
