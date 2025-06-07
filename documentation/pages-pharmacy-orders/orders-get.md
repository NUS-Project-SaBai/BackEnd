# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - Example: Pharmacy > Orders > index.js

- **Purpose on Frontend**:  
  Fetches all orders with 'pending' status

---

## API Endpoint: `/orders?order_status=PENDING`

### Overview
- **Description**:  
  The /orders endpoint is currently a mess. Without a 'order_status' query param it works as per normal, returning a response with all orders in the database. However, when an order_status is specified, what is does now is that it fetches all the orders and all the diagnoses, and bundles it together and gives it to the frontend.
- **HTTP Method**:  
  GET

---

### Request Details

#### Query Parameters
- **Parameter Name**: order_status. example value: 'pending'

#### Request Body
- **Structure**:  
  N/A

---

### Response Details

#### Response Structure
- **Status Codes**:  
  List possible status codes (200, 400, 500, etc.) and their meanings.
- **Sample Response**:  
  ```json
  "orders": [
    {
      "id": 1,
      "consult": 1,
      "visit": {
        "id": 1,
        "patient": {
          "model": "clinicmodels.patient",
          "pk": 1,
          "village_prefix": "TT",
          "name": "Noah Seethor",
          "identification_number": "",
          "contact_no": "",
          "gender": "Female",
          "date_of_birth": "2025-02-14T00:00:00Z",
          "poor": "No",
          "bs2": "No",
          "sabai": "No",
          "drug_allergy": "None",
          "face_encodings": "",
          "picture": "http://localhost:8080/media/offline_pictures/patient_screenshot_EzAGLoT.jpg",
          "filter_string": "TT0001TT1  Noah Seethor",
          "patient_id": "TT0001",
          "confidence": ""
        },
        "date": "2025-02-12T12:46:25.935590Z",
        "status": "started"
      },
      "medication_review": {
        "id": 2,
        "approval": {
          "auth0_id": "",
          "username": "",
          "email": "",
          "nickname": ""
        },
        "medicine": {
          "id": 1,
          "medicine_name": "drugs",
          "quantity": 1000,
          "notes": "nth"
        },
        "quantity_changed": -12,
        "quantity_remaining": 988,
        "date": "2025-02-12T13:17:17.489938Z",
        "order_status": "PENDING"
      },
      "notes": "eat",
      "remarks": null
    }
  ],
  "diagnoses": [
    {
      "id": 1,
      "consult": {
        "id": 1,
        "visit": {
          "id": 1,
          "patient": {
            "model": "clinicmodels.patient",
            "pk": 1,
            "village_prefix": "TT",
            "name": "Noah Seethor",
            "identification_number": "",
            "contact_no": "",
            "gender": "Female",
            "date_of_birth": "2025-02-14T00:00:00Z",
            "poor": "No",
            "bs2": "No",
            "sabai": "No",
            "drug_allergy": "None",
            "face_encodings": "",
            "picture": "http://localhost:8080/media/offline_pictures/patient_screenshot_EzAGLoT.jpg",
            "filter_string": "TT0001TT1  Noah Seethor",
            "patient_id": "TT0001",
            "confidence": ""
          },
          "date": "2025-02-12T12:46:25.935590Z",
          "status": "started"
        },
        "doctor": {
          "auth0_id": "auth0|653a8f84d77e7cf783f83333",
          "username": "auth0|653a8f84d77e7cf783f83333",
          "email": "sabai@nuscomputing.com",
          "nickname": "sabai"
        },
        "prescriptions": [
          {
            "id": 1,
            "consult": 1,
            "visit": {
              "id": 1,
              "patient": {
                "model": "clinicmodels.patient",
                "pk": 1,
                "village_prefix": "TT",
                "name": "Noah Seethor",
                "identification_number": "",
                "contact_no": "",
                "gender": "Female",
                "date_of_birth": "2025-02-14T00:00:00Z",
                "poor": "No",
                "bs2": "No",
                "sabai": "No",
                "drug_allergy": "None",
                "face_encodings": "",
                "picture": "http://localhost:8080/media/offline_pictures/patient_screenshot_EzAGLoT.jpg",
                "filter_string": "TT0001TT1  Noah Seethor",
                "patient_id": "TT0001",
                "confidence": ""
              },
              "date": "2025-02-12T12:46:25.935590Z",
              "status": "started"
            },
            "medication_review": {
              "id": 2,
              "approval": {
                "auth0_id": "",
                "username": "",
                "email": "",
                "nickname": ""
              },
              "medicine": {
                "id": 1,
                "medicine_name": "drugs",
                "quantity": 1000,
                "notes": "nth"
              },
              "quantity_changed": -12,
              "quantity_remaining": 988,
              "date": "2025-02-12T13:17:17.489938Z",
              "order_status": "PENDING"
            },
            "notes": "eat",
            "remarks": null
          }
        ],
        "date": "2025-02-12T13:17:17.487418Z",
        "past_medical_history": "help",
        "consultation": "meep",
        "plan": "e",
        "referred_for": null,
        "referral_notes": null,
        "remarks": null
      },
      "details": "lol",
      "category": "Cardiovascular"
    }
  ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - Complete Order with all fields
  - Complete diagnosis with all fields
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - The Orders part is still ok
  - The sin is in the Diagnoses part, since we only really need the 'category' and 'details' fields

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
    `loadPendingOrders`
- **How**:  
    1. Parsing the bundled data to separate into orders and diagnoses. 
    2. For each order rendered, the consult_id associated with the order is extracted
    3. This consult_id is then used to filter the diagnoses to render the ones related to the order
- **Example (if applicable)**:  
    N/A

#### Processing on the Backend
- **Where**:  
    orders_view
- **How**:  
    1. All orders are fetched
    2. A list of consult ids are extracted
    3. This list is then used to filter all diagnoses to retrieve a list of diagnoses that have any of the ids in the list
    4. Data is serialised, bundled together, then sent over
- **Example (if applicable)**:  
    N/A

---

### Additional Notes
- **If Any**:  