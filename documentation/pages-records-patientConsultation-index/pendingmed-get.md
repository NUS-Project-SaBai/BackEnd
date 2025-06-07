# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/medications/${orderFormDetails.medicine}?order_status=PENDING`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  gets the medication quantity where order_status of the medicine is pending
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**: orderFormDetails.medicine (integer)

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
  {
  "id": 11,
  "medicine_name": "Paracetamol 500mg",
  "quantity": 24924,
  "notes": ""
  }
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - id
  - medicine_name
  - quantity
  - notes

  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - quantity requested
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Collect the pending quantity requested 
- **How**:  
  
- **Example**:  
  Alert when (pending order + current_order) > stock

#### Processing on the Backend
- **Where**:  
  Under medication_view?
- **How**:  
  Collect all medication objects

  Using MedicationSerializer, serialize medication and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*