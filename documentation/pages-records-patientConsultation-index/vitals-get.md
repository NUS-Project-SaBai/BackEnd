# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/vitals?visit=${visitID}`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  gets visit id of patient to generate details of patient's vitals
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
    "id": 470,
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
        "date_of_birth": "2004-12-25T00:00:00Z",
        "poor": "No",
        "bs2": "No",
        "sabai": "No",
        "drug_allergy": "no",
        "face_encodings": "",
        "picture": "",
        "filter_string": "TK0485TK485 ",
        "patient_id": "TK0485",
        "confidence": ""
      },
      "date": "2024-12-09T04:29:18.347935Z",
      "status": "started"
    },
    "height": "",
    "weight": "",
    "temperature": null,
    "systolic": "",
    "diastolic": "",
    "heart_rate": "",
    "hemocue_count": null,
    "diabetes_mellitus": "Haven't Asked / Not Applicable",
    "urine_test": null,
    "blood_glucose_non_fasting": null,
    "blood_glucose_fasting": null,
    "left_eye_degree": "",
    "right_eye_degree": "",
    "left_eye_pinhole": "",
    "right_eye_pinhole": "",
    "gross_motor": null,
    "red_reflex": null,
    "scoliosis": null,
    "pallor": null,
    "oral_cavity": null,
    "heart": null,
    "abdomen": null,
    "lungs": null,
    "hernial_orifices": null,
    "pubarche": "Haven't Asked / Not Applicable",
    "pubarche_age": null,
    "thelarche": "Haven't Asked / Not Applicable",
    "thelarche_age": null,
    "menarche": "Haven't Asked / Not Applicable",
    "menarche_age": null,
    "voice_change": "Haven't Asked / Not Applicable",
    "voice_change_age": null,
    "testicular_growth": "Haven't Asked / Not Applicable",
    "testicular_growth_age": null,
    "others": null
  }
  ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - id
  - visit fields
  - height
  - weight
  - temp
  - systolic
  - diastolic
  - heart_rate
  - hemocue_count
  - diabetes_mellitus
  - urine_test
  - blood_glucose_non_fasting
  - blood_glucose_fasting
  - left_eye_degree
  - right_eye_degree
  - left_eye_pinhole
  - right_eye_pinhole
  - gross_motor
  - red_reflex
  - scoliosis
  - pallor
  - oral_cavity
  - heart
  - abdomen
  - lungs
  - hernial_orifices
  - pubarche
  - pubarche_age
  - thelarche
  - thelarche_age
  - menarche
  - manarche_age
  - voice_change
  - voice_change_age
  - testicular_growth
  - testicular_growth_age
  - others

  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - All fields
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Consult data collected and used under SetVitals(), thereafter used to generate height-weight graph
- **How**:  
  Used for VitalsTable and height-weight graph
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  Under vitals_view
- **How**:  
  Get all vital objects, query param by visit and filter all vitals based on visit

  Using VitalSerializer, serialize vitals and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*