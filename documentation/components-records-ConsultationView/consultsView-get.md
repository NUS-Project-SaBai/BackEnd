# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > records (view) > consultations > VIEW button

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - to display past consultation data like diagnosis, prescriptions and referrals
---

## API Endpoint: `/diagnosis?consult=${consult.id}`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  See history consult
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**: consult_id (integers)

#### Request Body
- **Structure**:  
  Provide a sample JSON structure if applicable.

---

### Response Details

#### Response Structure
- **Status Codes**:  
  List possible status codes (200, 400, 500, etc.) and their meanings.
    - 200: OK request went through
    - 400: Bad Request
    - 500: Internal Server Error: Backend ran into some issue
    - 401: Unauthorised: Authentication fail
- **Sample Response**:  
  ```json
        [
    {
        "id": 849,
        "consult": {
        "id": 500,
        "visit": {
            "id": 436,
            "patient": {
            "model": "clinicmodels.patient",
            "pk": 420,
            "village_prefix": "TK",
            "name": "patient_name",
            "identification_number": "N/A",
            "contact_no": "contact_number",
            "gender": "Female",
            "date_of_birth": "year-month-dayT00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "NO",
            "face_encodings": "0face_encoding",
            "picture": "jpg picture",
            "filter_string": "TK000TK000 number name",
            "patient_id": "TK000",
            "confidence": ""
            },
            "date": "2024-12-09T03:37:04.718516Z",
            "status": "started"
        },
        "doctor": {
            "auth0_id": "auth0|6751fb454faa790dca4f50bd",
            "username": "auth0|6751fb454faa790dca4f50bd",
            "email": "dr_email",
            "nickname": "dr_nickname"
        },
        "prescriptions": [
            {
            "id": 615,
            "consult": 500,
            "visit": {
                "id": 436,
                "patient": {
                "model": "clinicmodels.patient",
                "pk": 420,
                "village_prefix": "TK",
                "name": "name",
                "identification_number": "N/A",
                "contact_no": "number",
                "gender": "Female",
                "date_of_birth": "1994-10-00T00:00:00Z",
                "poor": "No",
                "bs2": "No",
                "sabai": "No",
                "drug_allergy": "NO",
                "face_encodings": "face-encoding",
                "picture": "jpg image",
                "filter_string": "TK0000TK000 number name",
                "patient_id": "TK0420",
                "confidence": ""
                },
                "date": "2024-12-09T03:37:04.718516Z",
                "status": "started"
            },
            "medication_review": {
                "id": 1490,
                "approval": {
                "auth0_id": "auth0|674d4247e6d978154d4e055e",
                "username": "auth0|674d4247e6d978154d4e055e",
                "email": "email",
                "nickname": "nickname"
                },
                "medicine": {
                "id": 55,
                "medicine_name": "Fluconazole (oral)",
                "quantity": 173,
                "notes": ""
                },
                "quantity_changed": -1,
                "quantity_remaining": 176,
                "date": "2024-12-09T05:19:48.835353Z",
                "order_status": "APPROVED"
            },
            "notes": "To take 1 tablet for candida infection",
            "remarks": null
            },
            {
            "id": 616,
            "consult": 500,
            "visit": {
                "id": 436,
                "patient": {
                "model": "clinicmodels.patient",
                "pk": 420,
                "village_prefix": "TK",
                "name": "name",
                "identification_number": "N/A",
                "contact_no": "number",
                "gender": "Female",
                "date_of_birth": "1994-10-00T00:00:00Z",
                "poor": "No",
                "bs2": "No",
                "sabai": "No",
                "drug_allergy": "NO",
                "face_encodings": "face-encoding",
                "picture": "jpg picture",
                "filter_string": "TK0000TK000 number name",
                "patient_id": "TK0420",
                "confidence": ""
                },
                "date": "2024-12-09T03:37:04.718516Z",
                "status": "started"
            },
            "medication_review": {
                "id": 1491,
                "approval": {
                "auth0_id": "auth0|674d4247e6d978154d4e055e",
                "username": "auth0|674d4247e6d978154d4e055e",
                "email": "email",
                "nickname": "nickname"
                },
                "medicine": {
                "id": 56,
                "medicine_name": "Triple combination cream (Combiderm/Dermagen) 15gm",
                "quantity": 5,
                "notes": ""
                },
                "quantity_changed": -1,
                "quantity_remaining": 9,
                "date": "2024-12-09T05:19:53.972967Z",
                "order_status": "APPROVED"
            },
            "notes": "Apply to PV region 2 times per day as required",
            "remarks": null
            }
        ],
        "date": "2024-12-09T05:03:23.081584Z",
        "past_medical_history": "as per earlier entry",
        "consultation": "consultdetails",
        "plan": "consultplan",
        "referred_for": null,
        "referral_notes": null,
        "remarks": null
        },
        "details": "consult details",
        "category": "consult category(dropdown)"
    }
    ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
    - patient_id
    - consult_id
    - visit details (registration fields)
    - doctor fields (auth0_id, username, email, nickname)
    - prescription details (recalls patient registration fields)
    - date
    - medication_review (approval of meds)
    - medicine details (quant changed/remaining and notes)
    - consult_id (again)
    - visit details (again with registration fields)
    - past_medical_history
    - consultation
    - plan
    - referred_for
    - referral_notes
    - remarks
    - diagnosis details and category
  - ...
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
    - doctor (consult done by)
    - past_medical_details
    - consultation
    - plan
    - referred_for
    - referred_notes (same as referral_notes)
    - remarks

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  under async function fetchDiagnosis
- **How**:  
  will fetch diagnosis and consults given consult_id

#### Processing on the Backend
- **Where**:  
  Processing done in consult_view and diagnosis_view, with help of ConsultSerializer
- **How**:  
  In ConsultView, query param visit id and filter all consults using visit id
  In DiagnosisView, query param consult_id and filter all diagnosis using consult_id

  Serialise using ConsultSerializer and DiagnosisSerializer and returns response

---

### Additional Notes
- **If Any**:  

*End of Template*