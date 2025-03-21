# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records page

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - to display patients in order of registration time
---

## API Endpoint: `/patients`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  See past registered patients, to create vitals/consults for them if needed
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**: n/a

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
        "model": "clinicmodels.patient",
        "pk": 1776,
        "village_prefix": "PC",
        "name": "xx",
        "identification_number": "23456",
        "contact_no": "44",
        "gender": "Male",
        "date_of_birth": "2020-11-11T00:00:00Z",
        "poor": "No",
        "bs2": "No",
        "sabai": "No",
        "drug_allergy": "na",
        "face_encodings": "",
        "picture": "jpg image",
        "filter_string": "PC1776PC1776 44 xx",
        "patient_id": "PC1776",
        "confidence": ""
    }
    ]
  ```
  will have the entire lists of patients, above is just one of the many patients

#### Data Fetched by the Frontend
- **Complete Data Set**:  
    - pk -- patientid num
    - village_prefix
    - name
    - iden number
    - contact number
    - gender
    - date_of_birth
    - poor
    - bs2
    - sabai
    - drug_allergy
    - face_encodings
    - picture
    - patient_id
    - confidence
  - ...
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
    All fields above 
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  under function PatientList()
- **How**:  
  will fetch patients in groups of 10

#### Processing on the Backend
- **Where**:  
  Processing done in patient_view
- **How**:  
  In ConsultView, query param visit id and filter all consults using visit id
  In DiagnosisView, query param consult_id and filter all diagnosis using consult_id

  Serialise using ConsultSerializer and DiagnosisSerializer and returns response

  In PatientView, order all patients by their PK, query param name to filter by name, and/or query param code to filter by village_prefix

  Serialise using PatientSerializer and return serialised response

---

### Additional Notes
- **If Any**:  

*End of Template*