"""
Documentation for Google Drive API:
https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.html
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
from sabaibiometrics.settings import (
    GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE,
    GOOGLE_DRIVE_FILE_ID,
)
import os
import tempfile
import requests


SCOPES = ["https://www.googleapis.com/auth/drive"]


def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return creds


def upload_file(uploaded_file, labeled_filename):
    creds = authenticate()  # credentials to authenticate
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": labeled_filename, "parents": [GOOGLE_DRIVE_FILE_ID]}

    # Temporarily save the file if it's not already saved
    if isinstance(uploaded_file, (str, bytes, os.PathLike)):
        file_path = uploaded_file
    else:
        file_path = os.path.join(tempfile.gettempdir(), labeled_filename)
        with open(file_path, "wb") as temp_file:
            # Read in chunks if necessary
            for chunk in iter(
                lambda: uploaded_file.read(1024 * 1024), b""
            ):  # Read 1MB chunks
                temp_file.write(chunk)

    file = (
        service.files()
        .create(
            body=file_metadata,  # where to upload and name to upload as
            media_body=file_path,  # picture or document to upload
            fields="id, name",  # only return necessary fields
        )
        .execute()
    )

    # Optionally delete the temp file
    if not isinstance(uploaded_file, (str, bytes, os.PathLike)):
        os.remove(file_path)

    file_id = file.get("id")
    file_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return file_url


def download_file(url, output_filename):
    """
    Downloads a file from a Google Drive sharing URL and saves it locally.

    Args:
        url (str): The sharing URL of the file.
        output_filename (str): The name to save the downloaded file as.

    Returns:
        str: Path to the downloaded file.
    """
    # Extract file ID from the shared URL
    try:
        file_id = url.split("/d/")[1].split("/")[0]
    except IndexError:
        raise ValueError(
            "Invalid Google Drive URL format. Please provide a valid sharing link."
        )

    # Google Drive download link format
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dir_path = os.path.join(project_root, "media", "offline_files")
    os.makedirs(dir_path, exist_ok=True)
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(dir_path, output_filename)
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive chunks
                    file.write(chunk)
        return f"offline_files/{output_filename}"
    else:
        raise Exception(
            f"Failed to download file: {response.status_code}, {response.text}"
        )


def rename_file(file_url, new_name):
    """
    Renames a file on Google Drive.

    Args:
        file_url (str): The URL of the file to rename.
        new_name (str): The new name for the file.

    Returns:
        str: The new URL of the renamed file.
    """
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    # Extract file ID from the shared URL
    try:
        file_id = file_url.split("/d/")[1].split("/")[0]
    except IndexError:
        raise ValueError(
            "Invalid Google Drive URL format. Please provide a valid sharing link."
        )

    # Update the file's name
    updated_file = (
        service.files().update(fileId=file_id, body={"name": new_name}).execute()
    )

    if not updated_file or not updated_file.get("id"):
        raise ConnectionError("Failed to rename file on Google Drive.")

    return f"https://drive.google.com/file/d/{updated_file['id']}/view?usp=sharing"
