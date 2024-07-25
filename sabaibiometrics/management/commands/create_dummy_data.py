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

            #Create a User for the Consult doctor if it doesnt exist. This ensures
            #that a doctor is always available for creating related 'consult' 
            #records; reliabily referenced to the same doc. 
            
            doctor = CustomUser.objects.get(pk=1)
            

            #Number of patients and visits(max: 9) to create 
            num_patients = 100 
            visits_per_patient = 3 
            #loop to create multiple patients 
            for i in range(num_patients):
                patient_number = i + 1 
                
                patient_name = f"Patient_{patient_number}"
                identification_number = f"ID_{patient_number}"
                contact_no = f"123456789{patient_number}"
                gender = (["Male","Female"][patient_number % 2])
                date_of_birth = f"199{patient_number%10}-01-01"
                drug_allergy = (["None","Penicillin","Aspirin"][patient_number % 3])

                #Created a patient and assign it to the 'patient' variable 
                patient = Patient.objects.create(
                    village_prefix= "VPF",
                    name= patient_name,
                    identification_number= identification_number,
                    contact_no= contact_no,
                    gender= gender,
                    date_of_birth= date_of_birth,
                    drug_allergy= drug_allergy,
                    picture= "image/upload/v1715063294/ghynewr4gdhkuttombwc.jpg",
                )
                #nested loop to create multiple visits per patient  
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
                    
                    #Create vitals and link to the 'visit'
                    Vitals.objects.create(
                        visit= visit,
                        height= vitals_number,
                        weight= vitals_number, 
                        systolic= vitals_number,
                        diastolic= vitals_number,
                        temperature= vitals_number,
                        diabetes_mellitus= (["Yes","No"][visit_number % 2]),
                        heart_rate= visit_number,
                        urine_test= (["True","False"][visit_number % 2]),
                        hemocue_count= vitals_number,
                        blood_glucose= vitals_number,
                        left_eye_degree= f"+{vitals_number}",
                        right_eye_degree= f"+{vitals_number}",
                        left_eye_pinhole= f"+{vitals_number}",
                        right_eye_pinhole= f"+{vitals_number}",
                        others= "others",
                    )
                    #Create consult and link it to the 'visit' and 'doctor'
                    consult = Consult.objects.create(
                        visit= visit,
                        date= timezone.now(),
                        doctor= doctor, #Reference the doctor
                        past_medical_history= (["None","Hypertension","Diabetes"][visit_number % 3]),
                        consultation= "General checkup",
                        plan= "Follow-up in 6 months",
                        referred_for= "referred_for",
                        referral_notes= "referral_notes",
                        remarks= "remarks",
                    )

                    #Create a diagnosis and link it to the 'consult'
                    Diagnosis.objects.create(
                        consult= consult, 
                        details= "consult_details",
                        category= "consult_category",
                    )
                    #Create medication 
                    medication = Medication.objects.create(
                        medicine_name= random.choice(["Aspirin","Ibuprofen","Paracetamol"][visit_number % 3]),
                        quantity= patient_number,
                        notes= "Take as needed"
                    )
                    #Create an order and link it to the 'medication' and 'consult' 
                    Order.objects.create(
                        medicine= medication,
                        consult= consult,
                        quantity= patient_number,
                        notes= "order_notes",
                        remarks= "remarks",
                        order_status= (["Completed","Pending"][visit_number % 2]),
                    )

            self.stdout.write("Dummy data created successfully")
        except IntegrityError:
            self.stdout.write("Dummy data already exist")