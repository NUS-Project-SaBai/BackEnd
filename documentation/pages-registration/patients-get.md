# patients endpoint

---

**Frontend Location**:

- `pages/registration/index.js`

- **Purpose on Frontend**:
- patients endpoint retrieves all of the patients data to be used in RegistrationAutoSuggest components

---

## API Endpoint:

- `/patients`

### Overview

- **Description**:  
  Returns an array of JSON objects with all of the patients data
- **HTTP Method**:  
  GET
- **Authentication**:

---

### Request Details

#### URL Parameters

NIL

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
  "name": "paient_name",
  "identification_number": "",
  "contact_no": "",
  "gender": "Female",
  "date_of_birth": "1961-01-01T00:00:00Z",
  "poor": "No",
  "bs2": "No",
  "sabai": "No",
  "drug_allergy": "None",
  "face_encodings": "4f993c46-d194-40d2-90f4-79e21c556fee",
  "picture": "url_with_jpg",
  "filter_string": "SV1750SV1750  patient_name",
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
  - date_of_birth: date of birth in ISO 8061 format
  - poor:
  - bs2:
  - sabai: yes/no value of whether patient has sabai booklet
  - drug_allergy: string of drug allergy of patient
  - face_encodings: hash of patient's face_encodings
  - picture: URL of patient's captured image
  - filter_string:
  - patient_id: concatenation of village_prefix and pk
  - confidence: ""

#### Data Used by the Frontend

- **Relevant Data Subset**:
  used in RegistrationAutoSuggest components
- name
- village_prefix
- pk

---

### Data Processing Details

#### Processing on the Frontend

NIL

#### Processing on the Backend

- **Where**:  
  patient_view.py
- **How**:
  Order the patients object by desc pk and returns in a serialised format
- **Example**:

---

### Additional Notes

- **If Any**:
