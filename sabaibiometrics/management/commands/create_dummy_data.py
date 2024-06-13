from django.core.management.base import BaseCommand
from api.models import Patient, Visit, Vitals, Consult, Diagnosis, Medication, Order
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "Create dummy data"

    def handle(self, *args, **kwargs):
        try:
            Patient.objects.create(
                village_prefix= "VPF",
                name= "patient_name",
                identification_number= "identification_number",
                contact_no= "contact_no",
                gender= "gender",
                date_of_birth= "2021-01-01",
                drug_allergy= "drug_allergy",
                picture= "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
            )
            Visit.objects.create(
                patient= Patient.objects.get(id=1),
                date= "2021-01-01",
                status= "status",
            )
            Vitals.objects.create(
                visit= Visit.objects.get(id=1),
                height= "100.00",
                weight= "100.00",
                systolic= 100,
                diastolic= 100,
                temperature= "37.00",
                diabetes_mellitus= "Yes",
                heart_rate= 100,
                urine_test= "True",
                hemocue_count= "100.00",
                blood_glucose= "100.00",
                left_eye_degree= "+4",
                right_eye_degree= "+4",
                left_eye_pinhole= "+23",
                right_eye_pinhole= "+23",
                others= "others",
            )
            Consult.objects.create(
                visit= Visit.objects.get(id=1),
                date= "2021-01-01",
                doctor= User.objects.get(id=1),
                past_medical_history= "past_medical_history",
                consultation= "consultation",
                plan= "plan",
                referred_for= "referred_for",
                referral_notes= "referral_notes",
                remarks= "remarks",
            )
            Diagnosis.objects.create(
                consult= Consult.objects.get(id=1),
                details= "consult_details",
                category= "consult_category",
            )
            Medication.objects.create(
                medicine_name= "medicine_name",
                quantity= 1,
                notes= "notes",
                remarks= "remarks",
            )
            Order.objects.create(
                medicine= Medication.objects.get(id=1),
                consult= Consult.objects.get(id=1),
                quantity= 100,
                notes= "order_notes",
                remarks= "remarks",
                order_status= "status",
            )

            self.stdout.write("Dummy data created successfully")
        except IntegrityError:
            self.stdout.write("Dummy data already exist")