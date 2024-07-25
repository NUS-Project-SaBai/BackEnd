from django.core.management.base import BaseCommand
from api.models import Patient, Visit, Vitals, Consult, Diagnosis, Medication, Order, CustomUser
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils import timezone
import random 


class Command(BaseCommand):
    help = "Create dummy data"

    def handle(self, *args, **kwargs):
        try:
            '''
            #Create a User for the Consult doctor if it doesnt exist. This ensures
            #that a doctor is always available for creating related 'consult' 
            #records; reliabily referenced to the same doc. 
            '''

            # Get first user available
            doctor = CustomUser.objects.get(pk=1)
            

            # Number of patients and visits(max: 9) to create 
            num_patients = 100 
            visits_per_patient = 3 
            
            # loop to create multiple patients 
            for i in range(num_patients):
                patient_number = i + 1 
        
                patient_name = f"Patient_{patient_number}"
                identification_number = f"ID_{patient_number}"
                contact_no = f"123456789{patient_number}"
                gender = (["Male","Female"][patient_number % 2])
                date_of_birth = f"{patient_number%100 + 1000}-01-01"
                drug_allergy = f"Allergy Medication {patient_number}"
                village_prefix = (["PC", "CA", "TT", "TK", "SV"][(patient_number - 1) // (num_patients // 5)])

                # Created a patient and assign it to the 'patient' variable 
                patient = Patient.objects.create(
                    village_prefix= village_prefix,
                    name= patient_name,
                    identification_number= identification_number,
                    contact_no= contact_no,
                    gender= gender,
                    date_of_birth= date_of_birth,
                    drug_allergy= drug_allergy,
                    picture= "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
                )
                # nested loop to create multiple visits per patient  
                for j in range(visits_per_patient):
                    visit_number = j + 1
                    
                    visit_date = f"2024-01-{visit_number}"
                    visit_status = (["Completed","Pending","Cancelled"][visit_number % 3])

                    visit = Visit.objects.create(
                        patient= patient,
                        date= visit_date,
                        status= visit_status,
                    )

                    vitals_number = patient_number + (visit_number / 10)
                    
                    # Create vitals and link to the 'visit'
                    Vitals.objects.create(
                        visit= visit,
                        height= vitals_number,
                        weight= vitals_number, 
                        systolic= vitals_number,
                        diastolic= vitals_number,
                        temperature= vitals_number,
                        diabetes_mellitus= (["Yes","No"][visit_number % 2]),
                        heart_rate= vitals_number,
                        urine_test= (["True","False"][visit_number % 2]),
                        hemocue_count= vitals_number,
                        blood_glucose= vitals_number,
                        left_eye_degree= f"+{vitals_number}",
                        right_eye_degree= f"+{vitals_number}",
                        left_eye_pinhole= f"+{vitals_number}",
                        right_eye_pinhole= f"+{vitals_number}",
                        others= f"others{vitals_number}",
                    )
                    # Create consult and link it to the 'visit' and 'doctor'
                    consult = Consult.objects.create(
                        visit= visit,
                        date= timezone.now(),
                        doctor= doctor, #Reference the doctor
                        past_medical_history= f"Medical Diagnosis {vitals_number}",
                        consultation= f"General Checkup {vitals_number}",
                        plan= f"Follow-up in {vitals_number} months",
                        referred_for= f"referred_for_{vitals_number}",
                        referral_notes= f"referral_notes_{vitals_number}",
                        remarks= f"remark_{vitals_number}"
                    )

                    # Create a diagnosis and link it to the 'consult'
                    Diagnosis.objects.create(
                        consult= consult, 
                        details= f"consult_details{vitals_number}",
                        category= f"consult_category{vitals_number}",
                    )
                    # Create medication 
                    medication = Medication.objects.create(
                        medicine_name= f"Medication {vitals_number}",
                        quantity= patient_number,
                        notes= f"Take {vitals_number} as needed"
                    )
                    # Create an order and link it to the 'medication' and 'consult' 
                    Order.objects.create(
                        medicine= medication,
                        consult= consult,
                        quantity= patient_number,
                        notes= f"order_notes{vitals_number}",
                        remarks= f"remark_{vitals_number}",
                        order_status= (["Completed","Pending"][visit_number % 2]),
                    )

            self.stdout.write("Dummy data created successfully")
        except IntegrityError:
            self.stdout.write("Dummy data already exist")