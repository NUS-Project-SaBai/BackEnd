from django.core.management.base import BaseCommand
from api.models import Patient, Visit, Vitals, Consult, Diagnosis, Medication, Order, CustomUser, MedicationReview
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone
import random 

class Command(BaseCommand):
    help = "Create dummy data"

    def handle(self, *args, **kwargs):
        try:
            '''
            Create a User for the Consult doctor if it doesn't exist. This ensures
            that a doctor is always available for creating related 'consult' 
            records; reliably referenced to the same doctor. 
            '''

            # Get first user available
            doctor = CustomUser.objects.get(pk=1)

            # Number of patients and visits to create
            num_patients = 100
            visits_per_patient = 3

            for i in range(num_patients):
                patient_number = i + 1

                # Create a patient
                patient = Patient.objects.create(
                    village_prefix=["PC", "CA", "TT", "TK", "SV"][(patient_number - 1) // (num_patients // 5)],
                    name=f"Patient_{patient_number}",
                    identification_number=f"ID_{patient_number}",
                    contact_no=f"123456789{patient_number}",
                    gender=["Male", "Female"][patient_number % 2],
                    date_of_birth=f"{patient_number % 100 + 1000}-01-01",
                    drug_allergy=f"Allergy Medication {patient_number}",
                    picture="image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
                )

                for j in range(visits_per_patient):
                    visit_number = j + 1

                    # Create a visit
                    visit = Visit.objects.create(
                        patient=patient,
                        date=f"2024-01-{visit_number:02d}",
                        status=["Completed", "Pending", "Cancelled"][visit_number % 3],
                    )

                    vitals_number = patient_number + (visit_number / 10)

                    # Create vitals
                    Vitals.objects.create(
                        visit=visit,
                        height=vitals_number,
                        weight=vitals_number,
                        systolic=vitals_number,
                        diastolic=vitals_number,
                        temperature=vitals_number,
                        diabetes_mellitus=["Yes", "No"][visit_number % 2],
                        heart_rate=vitals_number,
                        urine_test=["True", "False"][visit_number % 2],
                        hemocue_count=vitals_number,
                        blood_glucose=vitals_number,
                        left_eye_degree=f"+{vitals_number}",
                        right_eye_degree=f"+{vitals_number}",
                        left_eye_pinhole=f"+{vitals_number}",
                        right_eye_pinhole=f"+{vitals_number}",
                        others=f"others{vitals_number}",
                    )

                    # Create consult
                    consult = Consult.objects.create(
                        visit=visit,
                        date=timezone.now(),
                        doctor=doctor,
                        past_medical_history=f"Medical Diagnosis {vitals_number}",
                        consultation=f"General Checkup {vitals_number}",
                        plan=f"Follow-up in {vitals_number} months",
                        referred_for=f"referred_for_{vitals_number}",
                        referral_notes=f"referral_notes_{vitals_number}",
                        remarks=f"remark_{vitals_number}"
                    )

                    # Create a diagnosis
                    Diagnosis.objects.create(
                        consult=consult,
                        details=f"consult_details{vitals_number}",
                        category=f"consult_category{vitals_number}",
                    )

                    # Create medication
                    medication = Medication.objects.create(
                        medicine_name=f"Medication {vitals_number}",
                        quantity=patient_number,
                        notes=f"Take {vitals_number} as needed"
                    )

                    # Create medication review
                    medication_review = MedicationReview.objects.create(
                        approval=doctor,
                        quantity_changed=random.randint(-10, 10),
                        quantity_remaining=medication.quantity + random.randint(-5, 5),
                        medicine=medication,
                        date=timezone.now(),
                        order_status=random.choice(['APPROVED', 'PENDING', 'CANCELLED']),
                    )

                    # Create an order
                    Order.objects.create(
                        consult=consult,
                        notes=f"order_notes{vitals_number}",
                        remarks=f"remark_{vitals_number}",
                        medication_review=medication_review,
                    )

            self.stdout.write(self.style.SUCCESS("Dummy data created successfully"))
        except IntegrityError:
            self.stdout.write(self.style.ERROR("Dummy data already exists"))