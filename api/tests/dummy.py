post_patient_dummy = {
    "village_prefix": "VPF",
    "name": "patient_name",
    "identification_number": "identification_number",
    "contact_no": "contact_no",
    "gender": "gender",
    "date_of_birth": "2021-01-01",
    "drug_allergy": "drug_allergy",
}

post_visit_dummy = {"patient": 1, "date": "2021-01-01", "status": "status"}

post_vitals_dummy = {
    "visit": 1,
    "height": 100,
    "weight": 100,
    "systolic": 100,
    "diastolic": 100,
    "temperature": 37,
    "diabetes_mellitus": "Yes",
    "heart_rate": 100,
    "urine_test": "True",
    "hemocue_count": 100,
    "blood_glucose": 100,
    "left_eye_degree": "+4",
    "right_eye_degree": "+4",
    "left_eye_pinhole": "+23",
    "right_eye_pinhole": "+23",
    "others": "others",
}

post_consult_dummy = {
    "visit": 1,
    "date": "2021-01-01",
    "doctor": 1,
    "past_medical_history": "past_medical_history",
    "consultation": "consultation",
    "plan": "plan",
    "referred_for": "referred_for",
    "referral_notes": "referral_notes",
    "remarks": "remarks",
}

post_diagnosis_dummy = {
    "consult": 1,
    "details": "consult_details",
    "category": "consult_category",
}

post_medication_dummy = {
    "medicine_name": "medicine_name",
    "quantity": 1,
    "notes": "notes",
}

post_order_dummy = {
    "medicine": 1,
    "quantity": 100,
    "consult": 1,
    "notes": "order_notes",
    "remark": "order_remark",
    "order_status": "status",
}
