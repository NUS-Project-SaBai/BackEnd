# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient

---

## API Endpoint: `/medications`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  displays medication available and their stock 
- **HTTP Method**:  
  GET
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**:

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
    "id": 1,
    "medicine_name": "xxx",
    "quantity": 2723,
    "notes": "shbdfh"
  }
  ]
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
  - All fields
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Consult data collected and used under SetMedications(), thereafter used to check in OrderForm if quantity to be ordered < stock
- **How**:  
  Used for OrderForm
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  Under vitals_view
- **How**:  
  Get all medication objects

  Using MedicationSerializer, serialize medication and return serialized data
- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*