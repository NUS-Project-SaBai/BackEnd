from django.core.management.base import BaseCommand
from api.models import CustomUser, Patient, File, Consult, Diagnosis, Medication, MedicationReview, Order, Visit, Vitals


class Command(BaseCommand):
    help = "Create default users"

    def handle(self, *args, **kwargs):
        users = CustomUser.objects.all()
        File.objects.all().delete()
        MedicationReview.objects.all().delete()
        Medication.objects.all().delete()
        Diagnosis.objects.all().delete()
        Consult.objects.all().delete()
        Order.objects.all().delete()
        Visit.objects.all().delete()
        Vitals.objects.all().delete()
        Patient.objects.all().delete()
        users.delete()