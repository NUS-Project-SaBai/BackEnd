from sabaibiometrics.utils import jwt_decode_token
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os


def get_doctor_id(headers):
    if "Authorization" in headers:
        token = headers["Authorization"].split(" ")[1]
        payload = jwt_decode_token(token)
        doctor_id = payload.get("sub")
        return doctor_id


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'api/views/utils/annular-strata-433816-d1-4df090169a8a.json'

PARENT_FOLDER_ID = "1yYfYXACDQoJ5LX51C4r7_d850Tq37aJf"  # url for where to upload


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds


def upload_photo(file_path, labeled_filename):
    creds = authenticate()  # credentials to authenticate
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': labeled_filename,
        'parents': [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,  # where to upload and name to upload as
        media_body=file_path  # picture or document to upload
    ).execute()

    print(f"File uploaded successfully! ID: {file.get('id')}")


# calling the function, this will spam upload on start up
# upload_photo("api/views/utils/image.png")
