# visits endpoint

---

**Frontend Location**:

- `pages/registration/index.js`

**Purpose on Frontend**:

Adds a new visit for a specific patientID via a JSON object

---

## API Endpoint:

- `/visits`

### Overview

- **Description**:  
  Adds a new visit for a specific patientID via a JSON object
- **HTTP Method**:  
  POST
- **Authentication**:

---

### Request Details

#### URL Parameters

NIL

#### Query Parameters

NIL

#### Request Body

```json
{
  "patient": "integer",
  "status": "string",
  "visit_date": "string (DD MMMM YYYY HH:mm format)"
}
```

- **Structure**:

---

### Response Details

Returns the personal details of the patient associated with the patientID

#### Response Structure

- **Status Codes**:
  200, 400, 500
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

#### Processing on the Frontend

- **Where**:  
  submitNewVisit
- **How**:  
  Formats the new visit in a JSON object with 3 properties
- **Example**:
  - patient: patient.pk,
  - status: 'started',
  - visit_date: moment().format('DD MMMM YYYY HH:mm'),

#### Processing on the Backend

- **Where**:  
  visit_view.py
- **How**:  
  Uses the VisitSerializer's is_valid method to check whether response is valid and saves and returns corresponding response

---

### Additional Notes

- **If Any**:
