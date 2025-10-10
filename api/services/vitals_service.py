from api.models import Vitals


def list_vitals_by_visit_id(visit_id=None):
    if visit_id:
        return Vitals.objects.filter(visit=visit_id)
    return Vitals.objects.all()


def list_vitals_by_patient_id(patient_id=None):
    if patient_id:
        return Vitals.objects.filter(visit__patient__pk=patient_id)
    return Vitals.objects.all()


def get_vitals(pk):
    return Vitals.objects.get(pk=pk)


def create_vitals(data):
    return Vitals.objects.create(**data)


def update_vitals(vital, data):
    for key, value in data.items():
        if value != "":
            setattr(vital, key, value)
    vital.save()
    return vital


def delete_vitals(pk):
    Vitals.objects.get(pk=pk).delete()
