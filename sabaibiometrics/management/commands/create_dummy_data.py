from django.core.management.base import BaseCommand
from api.models import Patient, Visit, Vitals, Consult, Diagnosis, Medication, Order
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
            doctor, created = User.objects.get_or_create(
                username="doctor"
                defaults={"email":"doctor@example.com","password":"password"}
            )

            #Number of patients and visits to create 
            num_patients = 10 
            vists_per_patient = 3 
            #loop to create multiple patients 
            for i in range(num_patients): 
                patient_name = f"Patient_{i+1}"
                identification_number = f"ID_{i+1}"
                contact_no = f"123456789{i+1}"
                gender = random.choice(["Male","Female"])
                date_of_birth = f"199{i%10}-01-01"
                drug_allergy = random.choice(["None","Penicillin","Aspirin"])
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
                    visit_date = f"2024-01-{j+1}"
                    visit_status = random.choice(["Completed","Pending","Cancelled"])

                    visit = Visit.objects.create(
                        patient= patient,
                        date= visit_date,
                        status= visit_status,
                    )
                    #Create vitals and link to the 'visit' 
                    Vitals.objects.create(
                        visit= visit,
                        height= round(random.uniform(100.0,200.0),2),
                        weight= round(random.uniform(35.0,120.0),2),
                        systolic= random.randint(90,140),
                        diastolic= random.randint(60,90),
                        temperature= round(random.uniform(35.0,40.0),1),
                        diabetes_mellitus= random.choice(["Yes","No"]),
                        heart_rate= random.randint(60,100),
                        urine_test= random.choice(["True","False"]),
                        hemocue_count= round(random.uniform(10.0,15.0),1),
                        blood_glucose= round(random.uniform(70.0,120.0),1),
                        left_eye_degree= f"+{random.randint(0,6)}",
                        right_eye_degree= f"+{random.randint(0,6)}",
                        left_eye_pinhole= f"+{random.randint(0,4)}",
                        right_eye_pinhole= f"+{random.randint(0,4)}",
                        others= "others",
                    )
                    #Create consult and link it to the 'visit' and 'doctor'
                    consult = Consult.objects.create(
                        visit= visit,
                        date= timezone.now(),
                        doctor= doctor, #Reference the doctor
                        past_medical_history= random.choice(["None","Hypertension","Diabetes"]),
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
                        medicine_name= random.choice(["Aspirin","Ibuprofen","Paracetamol"]),
                        quantity= random.randint(1,10),
                        notes= "Take as needed",
                        remarks= "common pain reliever",
                    )
                    #Create an order and link it to the 'medication' and 'consult' 
                    Order.objects.create(
                        medicine= medication,
                        consult= consult,
                        quantity= random.randint(1,10),
                        notes= "order_notes",
                        remarks= "remarks",
                        order_status= random.choice(["Completed","Pending"]),
                    )

            self.stdout.write("Dummy data created successfully")
        except IntegrityError:
            self.stdout.write("Dummy data already exist")