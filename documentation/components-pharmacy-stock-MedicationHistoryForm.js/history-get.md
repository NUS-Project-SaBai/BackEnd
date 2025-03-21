# API Documentation Template

---
- **Frontend Location**:  
Pharmacy Stock Page, after adding meidicine on the "History" button beside the medicine

- **Purpose on Frontend**:  
Retrieves and display the history of the medicine changes

---

## API Endpoint: /medication_review?medication_pk={medication_pk}

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
See the history of the changes made to the medicine

- **HTTP Method**:  
GET

- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).
None
---

### Request Details

#### URL Parameters
- **Parameter Name**: Description, type, and example value.
- **Parameter Name**: Description, type, and example value.

#### Query Parameters
- **Parameter Name:** medication_pk (integers)

#### Request Body
- **Structure**:  
  Provide a sample JSON structure if applicable.
  N/A

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
      "id": 1,
      "approval": {
        "auth0_id": "auth0|653a8f84d77e7cf783f83333",
        "username": "auth0|653a8f84d77e7cf783f83333",
        "email": "sabai@nuscomputing.com",
        "nickname": "sabai"
      },
      "medicine": {
        "id": 1,
        "medicine_name": "xxx",
        "quantity": 2723,
        "notes": "shbdfh"
      },
      "quantity_changed": 2723,
      "quantity_remaining": 2723,
      "date": "2025-02-12T13:23:40.111676Z",
      "order_status": "APPROVED",
      "order": {
        "consult": null,
        "medication_review": null,
        "notes": "",
        "remarks": ""
      }
    }
  ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - doctor_id
  - doctor_id fields (auth0_id, username, email, nickname)
  - medicine_id
  - medicine_name
  - quantity_changed
  - quantity_remaining
  - date
  - order_status
  - order (all fields - consult, medication_review, notes, remarks)

  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - approval
  - patient_name = history.order.consult?.visit.patient.name || 'NA' ;
  - doctor = history.order.consult?.doctor.nickname || 'NA';
  - qty_changed
  - qty_remaining
  - time

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
under the `renderRows` function
- **How**:  
  - sort data by date `new Date(b.date) - new Date(a.date))`
  - changes patient_name and doctor_name based on whether nickname available or not
  - format time
- **Example**: 
  ```java
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .map(history => {
        const approval = history.approval.nickname;
        const patient_name = history.order.consult?.visit.patient.name || 'NA';
        const doctor = history.order.consult?.doctor.nickname || 'NA';
        const qty_changed = history.quantity_changed;
        const qty_remaining = history.quantity_remaining;
        const time = moment(history.date).format('DD MMMM YYYY HH:mm');
  ```
  

#### Processing on the Backend
- **Where**:  
  Processing done in  medication_review_view, with help of MedicationReviewSerializer
- **How**:  
  - Get all MedicationReview objects
  - Filter for medication_pk that is being requested from query params
  - Prefetch order
  - Serializer serializes, return response

---

### Additional Notes
- **If Any**:  

*End of Template*