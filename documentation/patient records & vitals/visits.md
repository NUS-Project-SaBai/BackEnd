# visits endpoint

---

**Frontend Location**:

- `pages/records/patient-record/index.js`
- `pages/records/patient-vitals/index.js

**Purpose on Frontend**:

- visits endpoint retrieves data for `patientID`; patient id is determined by the route

---

## API Endpoint: `/vists?patient={patientID}`

### Overview

- **Description**:  
  Returns a JSON object with the patients details and visits (if any)
- **HTTP Method**:  
  GET
- **Authentication**:

---

### Request Details

#### URL Parameters

NIL

#### Query Parameters

- **patientID**: primary key of the patient, integer, "1750"

#### Request Body

NIL

- **Structure**:

---

### Response Details

Returns the personal details of the patient associated with the patientID

#### Response Structure

- **Status Codes**:
  200, 400
- **Sample Response**:
  200:

```json
[
  {
    "id": 1840,
    "patient": {
      "model": "clinicmodels.patient",
      "pk": 1750,
      "village_prefix": "SV",
      "name": "patient_name",
      "identification_number": "",
      "contact_no": "",
      "gender": "Female",
      "date_of_birth": "ISO 8051 date and time format",
      "poor": "No",
      "bs2": "No",
      "sabai": "No",
      "drug_allergy": "None",
      "face_encodings": "4f993c46-d194-40d2-90f4-79e21c556fee",
      "picture": "url_with_jpg",
      "filter_string": "SV1750SV1750  patient_name",
      "patient_id": "SV1750",
      "confidence": ""
    },
    "date": "ISO 8601 date and time format",
    "status": "started"
  }
]
```

404:

```
Error: Request failed with status code 404
```

#### Data Fetched by the Frontend

- **Complete Data Set**:  
  List all fields that are currently sent over the API.

  - visit: ID of the visit (if any)
  - pk: primary key & paitentID
  - village_prefix: patient's village
  - name": name of patient
  - identification_number": Cambodian identification number
  - contact_no: Cambodian contact number
  - gender: gender of patient
  - date_of_birth": date of birth in ISO 8061 format
  - poor:
  - bs2:
  - sabai: yes/no value of whether patient has sabai booklet
  - drug_allergy: string of drug allergy of patient
  - face_encodings: hash of patient's face_encodings
  - picture: URL of patient's captured image
  - filter_string:
  - patient_id: concatenation of village_prefix and pk
  - confidence: ""
  - date: date of visit in ISO 8061 format
  - status: current status of the visit: max 100 characters

#### Data Used by the Frontend

- ID: visit ID (if any) (index.js)

### Data Processing Details

#### Processing on the Frontend

- **Where**:  
  Specify the component or module handling the processing.
- **How**:  
  Explain what processing is being done on the data (e.g., filtering, formatting).
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend

- **Where**:  
  Specify which part of the backend handles data processing (e.g., in the view, serializer, or a dedicated service).
- **How**:  
  Outline what transformations, validations, or business logic is applied to the data.
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes

- **If Any**:
