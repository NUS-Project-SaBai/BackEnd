# API Documentation Template

---
- **Frontend Location**:  
  Specify the page or component where this API is called.
  - patient records > CREATE under consultations > Submit button for consults

- **Purpose on Frontend**:  
  Describe briefly why the frontend needs this API call (e.g., to display data, to perform an action, etc.).
  - upon pressing create button, user would be brought to the consultations page where users can see more details of the patients and create a consultation for the patient
  - this helps to submit the consultation done by the doctor

---

## API Endpoint: `/consults`

### Overview
- **Description**:  
  A brief summary of what this API endpoint does.
  posts consultation done by doctor
- **HTTP Method**:  
  POST
- **Authentication**:  
  Describe if this endpoint requires authentication (e.g., JWT, API keys).

---

### Request Details

#### URL Parameters

#### Query Parameters
- **Parameter Name**:

#### Request Body
- **Structure**:  
  Provide a sample JSON structure if applicable.
  ```json
    [
      const combinedPayload = {
        consult: formPayload,
        diagnoses: diagnosesPayload,
        orders: ordersPayload,
      }
    ]
  ```

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

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  List all fields that are currently sent over the API.
  - consult
  - diagnoses
  - orders
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  List only the fields that the frontend actually uses.
  - All fields
---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  Posts consults data, then clear local storage
- **How**:  
  Router pushes records
- **Example**:  
  Describe any transformation or manipulation applied.

#### Processing on the Backend
- **Where**:  
  None?
- **How**:  

- **Example**:  
  Provide details on the logic or algorithms used to process data before sending the response.

---

### Additional Notes
- **If Any**:  

*End of Template*