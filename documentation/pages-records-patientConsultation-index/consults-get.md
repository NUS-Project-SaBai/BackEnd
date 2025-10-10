# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/consults?visit=${visitID}`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  gets patient id of patient to generate details of patient's visit
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**: visit_id (integer)

#### Request Body
- **Structure**:  
  Provide a sample JSON structure if applicable. n/a

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
    "id": 535,
    "visit": {
      "id": 501,
      "patient": {
        "model": "clinicmodels.patient",
        "pk": 485,
        "village_prefix": "TK",
        "name": "name",
        "identification_number": "",
        "contact_no": "",
        "gender": "Female",
        "date_of_birth": "year-12-25T00:00:00Z",
        "poor": "No",
        "bs2": "No",
        "sabai": "No",
        "drug_allergy": "no",
        "face_encodings": "abcde",
        "picture": "jpg",
        "filter_string": "TK0485TK485 number name",
        "patient_id": "TK0485",
        "confidence": ""
      },
      "date": "2024-12-09T04:29:18.347935Z",
      "status": "started"
    },
    "doctor": {
      "auth0_id": "auth0|6751fb7a4faa790dca4f50ca",
      "username": "auth0|6751fb7a4faa790dca4f50ca",
      "email": "drEmail",
      "nickname": "drNickname"
    },
    "prescriptions": [
      {
        "id": 655,
        "consult": 535,
        "visit": {
          "id": 501,
          "patient": {
            "model": "clinicmodels.patient",
            "pk": 485,
            "village_prefix": "TK",
            "name": "",
            "identification_number": "",
            "contact_no": "",
            "gender": "Female",
            "date_of_birth": "year-12-25T00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "no",
            "face_encodings": "",
            "picture": "",
            "filter_string": "TK0485TK485 number name",
            "patient_id": "TK0485",
            "confidence": ""
          },
          "date": "year-12-09T04:29:18.347935Z",
          "status": "started"
        },
        "medication_review": {
          "id": 1536,
          "approval": {
            "auth0_id": "auth0|674d4247e6d978154d4e055e",
            "username": "auth0|674d4247e6d978154d4e055e",
            "email": "email",
            "nickname": "nickname"
          },
          "medicine": {
            "id": 21,
            "medicine_name": "Doxycycline 100mg",
            "quantity": 1198,
            "notes": ""
          },
          "quantity_changed": -30,
          "quantity_remaining": 1226,
          "date": "2024-12-09T06:55:35.467102Z",
          "order_status": "APPROVED"
        },
        "notes": "",
        "remarks": null
      },
      {
        "id": 656,
        "consult": 535,
        "visit": {
          "id": 501,
          "patient": {
            "model": "clinicmodels.patient",
            "pk": 485,
            "village_prefix": "TK",
            "name": "",
            "identification_number": "",
            "contact_no": "",
            "gender": "Female",
            "date_of_birth": "year-12-25T00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "no",
            "face_encodings": "",
            "picture": "",
            "filter_string": "TK0485TK485 number name",
            "patient_id": "TK0485",
            "confidence": ""
          },
          "date": "2024-12-09T04:29:18.347935Z",
          "status": "started"
        },
        "medication_review": {
          "id": 1537,
          "approval": {
            "auth0_id": "auth0|674d4247e6d978154d4e055e",
            "username": "auth0|674d4247e6d978154d4e055e",
            "email": "email",
            "nickname": "nickname"
          },
          "medicine": {
            "id": 46,
            "medicine_name": "",
            "quantity": 26,
            "notes": ""
          },
          "quantity_changed": -1,
          "quantity_remaining": 28,
          "date": "2024-12-09T06:55:40.554951Z",
          "order_status": "APPROVED"
        },
        "notes": "",
        "remarks": null
      },
      {
        "id": 657,
        "consult": 535,
        "visit": {
          "id": 501,
          "patient": {
            "model": "clinicmodels.patient",
            "pk": 485,
            "village_prefix": "TK",
            "name": "name",
            "identification_number": "",
            "contact_no": "",
            "gender": "Female",
            "date_of_birth": "year-12-25T00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "no",
            "face_encodings": "",
            "picture": "",
            "filter_string": "TK0485TK485 number name",
            "patient_id": "TK0485",
            "confidence": ""
          },
          "date": "2024-12-09T04:29:18.347935Z",
          "status": "started"
        },
        "medication_review": {
          "id": 1538,
          "approval": {
            "auth0_id": "auth0|674d4247e6d978154d4e055e",
            "username": "auth0|674d4247e6d978154d4e055e",
            "email": "email",
            "nickname": "nickname"
          },
          "medicine": {
            "id": 58,
            "medicine_name": "",
            "quantity": 63,
            "notes": ""
          },
          "quantity_changed": -1,
          "quantity_remaining": 67,
          "date": "2024-12-09T06:55:44.082626Z",
          "order_status": "APPROVED"
        },
        "notes": "",
        "remarks": null
      },
      {
        "id": 658,
        "consult": 535,
        "visit": {
          "id": 501,
          "patient": {
            "model": "clinicmodels.patient",
            "pk": 485,
            "village_prefix": "TK",
            "name": "",
            "identification_number": "",
            "contact_no": "",
            "gender": "Female",
            "date_of_birth": "year-12-25T00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "no",
            "face_encodings": "",
            "picture": "",
            "filter_string": "TK0485TK485 number name",
            "patient_id": "TK0485",
            "confidence": ""
          },
          "date": "2024-12-09T04:29:18.347935Z",
          "status": "started"
        },
        "medication_review": {
          "id": 1539,
          "approval": {
            "auth0_id": "auth0|674d4247e6d978154d4e055e",
            "username": "auth0|674d4247e6d978154d4e055e",
            "email": "email",
            "nickname": "name"
          },
          "medicine": {
            "id": 40,
            "medicine_name": "",
            "quantity": 130,
            "notes": ""
          },
          "quantity_changed": -30,
          "quantity_remaining": 80,
          "date": "2024-12-09T06:55:49.368604Z",
          "order_status": "APPROVED"
        },
        "notes": "",
        "remarks": null
      }
    ],
    "date": "2024-12-09T06:48:58.794862Z",
    "past_medical_history": "",
    "consultation": "",
    "plan": "",
    "referred_for": null,
    "referral_notes": null,
    "remarks": null
  }
  ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - id
  - visit fields
  - patient fields
  - date
  - status
  - doctor fields
  - prescription fields
      - consult_id
      - visit
      - patient fields
      - medication review
      - medicine fields

  Each medication would call id, consult and visit
  - date
  - past_medical_history
  - consultation
  - plan
  - referred_for
  - referral_notes
  - remarks

  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - All fields
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Consult data collected and used under SetConsults() and SetPrescriptions()
- **How**:  
  Used for ConsultsTable and PrescriptionsTable
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  Under consult_view
- **How**:  
  Get all consult objects, query param by visit and filter all visits related to visit_key

  Using ConsultSerializer, serialize consults and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*