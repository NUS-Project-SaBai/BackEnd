# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/visits?patient=${patientID}`

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
  [
  {
    "id": 9,
    "patient": {
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
    },
    "date": "2025-02-22T15:47:47.386315Z",
    "status": "started"
  },
  {
    "id": 8,
    "patient": {
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
    },
    "date": "2025-02-22T15:47:44.713918Z",
    "status": "started"
  }
  ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - visit_id
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
  - date
  - status --> "started"
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - uses all the data under SetVisits
  - all data is being used to generate multiple visits (if applicable)
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Visit data collected and used under SetVisits(), thereafter used for vitals generation
- **How**:  
  Patient is used for vitals
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  Under visit_view
- **How**:  
  Get all visit objects, query param by patient and filter all visits related to patients id, then order by latest visit id

  Using VisitSerializer, serialize visits and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*