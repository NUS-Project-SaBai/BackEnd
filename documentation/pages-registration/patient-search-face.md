# visits endpoint

---

**Frontend Location**:

- `pages/registration/index.js`

**Purpose on Frontend**:

- patients POST endpoint searches for a matching face jpg in the backend and retrieves the data

---

## API Endpoint:

- `/patients/search_face`

### Overview

- **Description**:  
  Searches for a matching JPG via a JSON object
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
  "picture": "URL of image"
}
```

- **Structure**:

---

### Response Details

#### Response Structure

- **Status Codes**:
  200, 400, 500
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
  "confidence": "filled in with face_encoding data"
}
```

404:

```
Error: Request failed with status code 404
```

#### Processing on the Frontend

- **Where**:  
  submitScan
- **How**:  
  Formats the screenshot of the patient's face in a JSON object with urlToFile helper function

#### Processing on the Backend

- **Where**:  
  patient_search_view.py
- **How**:
  1. filters the patients object based on the facial_encoding determined by the facial_recognition function
  2. Serialises data and returns corresponding response

---

### Additional Notes

- **If Any**:
