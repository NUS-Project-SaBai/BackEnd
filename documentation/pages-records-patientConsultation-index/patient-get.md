# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/patients/${patientID}`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  gets patient id of patient
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**: patient_id (integer)

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
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - pk
  - village_prefix
  - name
  - identification_number
  - contact_no
  - gender
  - date_of_birth
  - poor
  - bs2
  - sabai
  - drug_allergy
  - face_encodings
  - picture
  - filter_string
  - patient_id
  - confidence
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - uses all the data under SetPatient()
  - fields that can be seen in the page
    - village_id (village_prefix + patient_id)
    - name
    - age (date_of_birth)
    - drug allergies only displayed upon adding medicine orders

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Patient data collected and used under SetPatient(), thereafter being used for orderforms and to generate vitals, height-weight graph and gender
- **How**:  
  Patient is used for vitals, HW graph
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  Under patient_view
- **How**:  
  Get all patients objects, order by pk, query param by name and village code and filter patients based on pk and village_code

  Using PatientSerializer, serialize patients and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*