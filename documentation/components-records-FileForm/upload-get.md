# API Documentation Template

---
- **Frontend Location**:  
  FileForm component in the Header component in the patient consultation page under patient records.

- **Purpose on Frontend**:  
  This API call retrieves all files and their information about the current patient to display to the user

---

## API Endpoint: `/files/`

### Overview
- **Description**:  
  Returns file information grouped by patient. Can filter by patient_pk and deleted status.
- **HTTP Method**:  
  GET

---

### Request Details

#### Query Parameters
- **patient_pk** (optional): Patient ID to filter files for a specific patient (e.g. 1)
- **deleted** (optional): Filter by deletion status
  - `"false"` (default): Only active/non-deleted files
  - `"true"`: Only deleted files
  - `"all"`: Both active and deleted files

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
- **Sample Response** (with `?patient_pk=1`):  
  ```json
    [
        {
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
            },
            "files": [
                {
                    "id": 1,
                    "patient_id": 1,
                    "file_path": null,
                    "offline_file": "/media/offline_files/TT001-2025-02-17-README.txt",
                    "file_name": "TT001-2025-02-17-README.txt",
                    "description": "Medical report",
                    "created_at": "2025-02-17T11:13:56.216801Z",
                    "is_deleted": false
                }
            ]
        }
    ]
  ```
  
- **Sample Response** (without `patient_pk` - returns all patients with files):  
  ```json
    [
        {
            "patient": { /* Patient 1 data */ },
            "files": [ /* Patient 1's files */ ]
        },
        {
            "patient": { /* Patient 2 data */ },
            "files": [ /* Patient 2's files */ ]
        }
    ]
  ```

#### Data Fetched by the Frontend
- **Complete Data Set**:  
  Returns an array of PatientFiles objects, each containing:
  - **patient**: Complete patient object with all fields (pk, name, village_prefix, date_of_birth, etc.)
  - **files**: Array of file objects, each with:
    - id
    - patient_id
    - file_path (url if online)
    - offline_file (local path if offline)
    - file_name
    - description
    - created_at
    - is_deleted
  
#### Data Used by the Frontend
- **Relevant Data Subset**:  
  From each PatientFiles object:
  - **patient.patient_id**: Patient identifier
  - **files[]**: Array of files for that patient
    - id
    - file_path
    - offline_file
    - file_name
    - description
    - created_at
    - is_deleted

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
  Processing is done in file_view (view layer) and file_service (service layer), with PatientFilesSerializer and FileSerializer
- **How**:  
  - Query params `patient_pk` and `deleted` are parsed and validated
  - `deleted` parameter is converted: "all" → None, "true" → True, "false" → False
  - If `patient_pk` provided: `file_service.get_patient_files()` returns single PatientFiles dict in a list
  - If no `patient_pk`: `file_service.list_patient_files()` groups all files by patient and returns list of PatientFiles dicts
  - PatientFilesSerializer serializes the data with nested PatientSerializer and FileSerializer (many=True)
  - Response always returns an array of PatientFiles objects for consistency


---

### Additional Notes
- **If Any**: 
