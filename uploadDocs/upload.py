from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'wip' #wip to take in json file from frontend
PARENT_FOLDER_ID = "wip" #wip to take in url for where to upload from frontend

def authenticate():
  creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  return creds

def upload_photo(file_path):
  creds = authenticate() #credentials to authenticate
  service = build('drive', 'v3', credentials=creds)

  file_metadata = {
    'name' : "Cat", #soon to take in name to upload 
    'parents' : [PARENT_FOLDER_ID]
  }

  file = service.files().create(
    body = file_metadata, #where to upload and name to upload as
    media_body=file_path #picture or document to upload
  ).execute() 

  print(f"File uploaded successfully! ID: {file.get('id')}")

#calling the function to upload melon
upload_photo("melon.jpg")