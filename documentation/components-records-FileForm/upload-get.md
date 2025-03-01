# API Documentation Template

---
- **Frontend Location**:  
  FileForm component in the Header component in the patient consultation page under patient records.

- **Purpose on Frontend**:  
  This API call retrieves all files and their information about the current patient to display to the user

---

## API Endpoint: `[Endpoint URL or Name]`

### Overview
- **Description**:  
  Returns file information ssociated with the given patient ID to display 
- **HTTP Method**:  
  GET

---

### Request Details

#### Query Parameters
- **Parameter Name**: patient_pk (e.g. 1)

#### Request Body
- **Structure**:  
  N/A

---

### Response Details

#### Response Structure
- **Status Codes**:  
    - 500: Internal Server Error: Uncaught error in system (VERY BAD)
    - 400: Bad Request: Request issues
    - 200: OK: All's good
- **Sample Response**:  
  ```json
    [
        {
            "id": 1,
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
                "filter_string": "TT0001TT1  Noah Seethor",
                "patient_id": "TT0001",
                "confidence": ""
            },
            "file_path": null,
            "offline_file": "/media/offline_files/TT001-2025-02-17-README.txt",
            "file_name": "TT001-2025-02-17-README.txt",
            "created_at": "2025-02-17T11:13:56.216801Z"
        }
    ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  All File Fields
  - file_path
  - offline_file
  - file_name
  - created_at

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
    - file_path
    - offline_file
    - file_name
    - created_at

---

### Data Processing Details

#### Processing on the Frontend
- **Where**:  
  under the `renderRows` function, ...
- **How**:  
    - Sorts files returns by createdAt: `files.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))`
    - Changes file link based on whether online link avaliable or not

#### Processing on the Backend
- **Where**:  
  All processing is done in the file_view, with the help of file_serializer
- **How**:  
  - All file objects are pulled
  - Patient PK is taken from Query Params and used to filter the files
  - Serialiser serialises, then seriaised response is returned


---

### Additional Notes
- **If Any**: 