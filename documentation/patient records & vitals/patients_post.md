# visits endpoint

---

**Frontend Location**:

- `pages/registration/index.js`

**Purpose on Frontend**:

- patients POST endpoint adds a new patient data to the backend

---

## API Endpoint:

- `/patients`

### Overview

- **Description**:  
  Adds a new patient for a specific patient via a JSON object
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
  "name": "string",
  "identification_number": "string",
  "gender": "string",
  "contact_no": "string",
  "date_of_birth": "string",
  "drug_allergy": "string",
  "village_prefix": "string",
  "poor": "boolean",
  "bs2": "boolean",
  "sabai": "boolean",
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

```

404:

```
Error: Request failed with status code 404
```

#### Processing on the Frontend

- **Where**:  
  submitNewPatient
- **How**:  
  Formats the new patient in a JSON object with properties

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
