from api.models import Visit
from django.db.models import OuterRef, Subquery, DateField, IntegerField, QuerySet
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

def annotate_with_last_visit(queryset: QuerySet) -> QuerySet:
    # get visits by patient id, ordered by date desc
    patient_visits_qs = Visit.objects.filter(patient_id=OuterRef('pk')).order_by('-date')
    # queryset of patient(s) annotated with their last visit date and id
    return queryset.annotate(
        last_visit_date=Subquery(patient_visits_qs.values('date')[:1], output_field=DateField()),
        last_visit_id=Subquery(patient_visits_qs.values('pk')[:1], output_field=IntegerField()),
    )
