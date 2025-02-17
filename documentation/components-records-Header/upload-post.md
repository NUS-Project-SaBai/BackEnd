# API Documentation Template

---
- **Frontend Location**:  
  Header component in the patient consultation page under records.

- **Purpose on Frontend**:  
  This API call uploads the submitted file given through the 'Upload Document' Button.

---

## API Endpoint: `/upload/`

### Overview
- **Description**:  
  Uploads a file to either the offline server, or to google drive. file info is then saved in db
- **HTTP Method**:  
  POST

---

### Request Details

#### Query Parameters
- None
#### Request Body
- **Structure**:  
  ```json
  {
    "file": "some file data",
    "filename": "patientIdentifier-currentDate-documentName",
    "patient_pk": 1
  }
  ```

---

### Response Details

#### Response Structure
- **Status Codes**:  
  - 500: Internal Server Error: Uncaught error in system (VERY BAD)
  - 400: Bad Request: Request Data issue
  - 200: OK: All's good
- **Sample Response**:  
  (Sample cannot be obtained as file upload not possible with debug page)

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  All File Fields
  - file_path = models.CharField(max_length=255, null=True)
  - offline_file = models.FileField(upload_to='offline_files/', null=True)
  - file_name = models.CharField(max_length=255)
  - created_at = models.DateTimeField(auto_now_add=True)

  + Patient Fields (for patient associated with File)
  ```json
  "patient": {
      "model": "clinicmodels.patient",
      "pk": 1,
      "village_prefix": "TT",
      "name": "john doe",
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
      "filter_string": "TT0001TT1  john doe",
      "patient_id": "TT0001",
      "confidence": ""
    }
  ```
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  None

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  under the 'uploadFile' function, ...
- **How**: 
  - document name is labelled: labeledDocumentName = `${patientIdentifier}-${currentDate}-${documentName}`;
  - Data on the file (e.g. file_name, patient_pk, current_date etc.) is put together in a FormData component 

#### Processing on the Backend
- **Where**:  
  All processing is done in the file_view, with the help of file_serializer
- **How**:  
  - File info is put into a dictionary
  - Depending on whether the system is in offline or online mode, the file is either saved directly into the db, or uploaded, then the file_path is stored
  - Serialiser serialises, then saves into db.

---

### Additional Notes
- **If Any**:  
