# API Documentation Template

---

- **Frontend Location**:  
  Header component in the patient consultation page under records.

- **Purpose on Frontend**:  
  This API call uploads the submitted file given through the 'Upload Document' Button.

---

## API Endpoint: `/files/`

### Overview

- **Description**:  
  Uploads one or more files for a patient. In online mode, files are uploaded to Google Drive and the `file_path` is stored; in offline mode, files are saved locally and `offline_file` is stored.
- **HTTP Method**:  
  POST
- **File Validation**:
  - Maximum file size: 25MB per file
  - File name cannot be empty or whitespace only

---

### Request Details

#### Query Parameters

- None

#### Request Body

- **Content-Type**: `multipart/form-data`
- **Fields**:

  - `files`: array of files (supports multiple)
  - `descriptions`: array of strings (one per file)
  - `patient_pk`: integer (patient ID)

  Example (pseudo):

  ```
  files: [<file1>, <file2>]
  descriptions: ["X-ray", "Lab report"]
  patient_pk: 1
  ```

---

### Response Details

#### Response Structure

- **Status Codes**:
  - 500: Internal Server Error: Uncaught error in system (VERY BAD)
  - 400: Bad Request: Request Data issue (invalid patient, no files, empty file name, file too large)
  - 201: Created: Files uploaded successfully
- **Sample Success Response** (201):
  ```
  "Uploaded 2 files:\nTT001-2025-02-17-X-ray.png\nTT001-2025-02-17-LabReport.pdf"
  ```
- **Sample Error Response** (400):
  ```json
  {
    "error": "Invalid patient 999"
  }
  ```
  or
  ```json
  {
    "error": "Invalid Files:\n\nfile.pdf - File is too large!\nimage.png - No name provided"
  }
  ```

#### Data Fetched by the Frontend

- Not applicable: POST returns a confirmation string for UX feedback.
  Use subsequent `GET /files/?patient_pk=...` to fetch uploaded file metadata.

---

### Data Processing Details

#### Processing on the Frontend

- **Where**:  
  under the `uploadFile` function, ...
- **How**:
  - document name is labelled: labeledDocumentName = `${patientIdentifier}-${currentDate}-${documentName}`;
  - Data on the file (e.g. file_name, patient_pk, current_date etc.) is put together in a FormData component

#### Processing on the Backend

- **Where**:  
  View: `api/views/file_view.py` (POST); Service: `api/services/file_service.py`
- **How**:
  - Extracts `files`, `descriptions`, and `patient_pk` from `multipart/form-data`
  - Validates arrays lengths and patient existence
  - Uploads to Google Drive or saves offline based on mode
  - Persists `File` records; returns a summary string of created filenames

---

### Additional Notes

- **If Any**:
