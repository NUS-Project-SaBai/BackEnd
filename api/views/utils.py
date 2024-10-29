from sabaibiometrics.utils import jwt_decode_token
from api.models import CustomUser
from sabaibiometrics.settings import OFFLINE
from googleapiclient.discovery import build
from google.oauth2 import service_account
from sabaibiometrics.settings import GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE, GOOGLE_DRIVE_FILE_ID
import os
import tempfile


def get_doctor_id(headers):
    if "Authorization" in headers:
        token = headers["Authorization"].split(" ")[1]
        payload = jwt_decode_token(token)
        doctor_id = payload.get("sub")
        return doctor_id
    elif "doctor" in headers and OFFLINE:
        auth0_id = CustomUser.objects.get(email=headers["doctor"]).auth0_id
        return auth0_id


SCOPES = ['https://www.googleapis.com/auth/drive']


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def upload_photo(uploaded_file, labeled_filename):
    creds = authenticate()  # credentials to authenticate
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': labeled_filename,
        'parents': [GOOGLE_DRIVE_FILE_ID]
    }

    file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)

    # Save the file temporarily
    with open(file_path, 'wb+') as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)

    file = service.files().create(
        body=file_metadata,  # where to upload and name to upload as
        media_body=file_path  # picture or document to upload
    ).execute()

    # Optionally delete the temp file
    os.remove(file_path)

    file_id = file.get('id')
    file_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return file_url
