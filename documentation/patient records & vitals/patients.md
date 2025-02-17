# patients endpoint

---

**Frontend Location**:

- `pages/records/patient-record/index.js`
- `pages/records/patient-vitals/index.js

- **Purpose on Frontend**:
- patiends endpoint retrieves data for `patientID`; patient id is determined by the route

---

## API Endpoint: `/patients/${patientID}`

### Overview

- **Description**:  
  Returns a JSON object with the patient data
- **HTTP Method**:  
  GET
- **Authentication**:  
  WIP - still trying to understand the authentication middleware in Django

---

### Request Details

#### URL Parameters

- **patientID**: primary key of the patient, integer, "1750"

#### Query Parameters

NIL

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
{
  "model": "clinicmodels.patient",
  "pk": 1750,
  "village_prefix": "SV",
  "name": "San Sarorn",
  "identification_number": "",
  "contact_no": "",
  "gender": "Female",
  "date_of_birth": "1961-01-01T00:00:00Z",
  "poor": "No",
  "bs2": "No",
  "sabai": "No",
  "drug_allergy": "None",
  "face_encodings": "4f993c46-d194-40d2-90f4-79e21c556fee",
  "picture": "https://res.cloudinary.com/dlusodadw/image/upload/v1734154609/uqybbpkxgdc9kbqyfzmr.jpg",
  "filter_string": "SV1750SV1750  San Sarorn",
  "patient_id": "SV1750",
  "confidence": ""
}
```

404:

```
Error: Request failed with status code 404
```

#### Data Fetched by the Frontend

- **Complete Data Set**:  
  List all fields that are currently sent over the API.

  - pk: primary key & paitentID
  - village_prefix: patient's village
  - name": name of patient
  - identification_number": Cambodian identification number
  - contact_no: Cambodian contact number
  - gender: gender of patient
  - date_of_birth": date of birth
  - poor: TO CLARIFY
  - bs2: TO CLARIFY
  - sabai: yes/no value of whether patient has sabai booklet
  - drug_allergy": string of drug allergy of patient
  - face_encodings: hash of patient's face_encodings
  - picture: URL of patient's captured image
  - filter_string: TO CLARIFY
  - patient_id: concatenation of village_prefix and pk
  - confidence: ""

#### Data Used by the Frontend

- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - Field 1: Description
  - Field 2: Description
  - Field 3: Description

---

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
