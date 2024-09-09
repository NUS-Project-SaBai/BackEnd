import io
import os
import uuid
import boto3
from botocore.exceptions import NoCredentialsError
# from sabaibiometrics.settings import (
#     AWS_SECRET_ACCESS_KEY,
#     AWS_ACCESS_KEY_ID,
#     AWS_REGION,
# )

BUCKET_NAME = "projectsabai"
FOLDER_NAME = "index"
s3 = None

# try:
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         region_name=AWS_REGION,
#     )
# except NoCredentialsError:
#     print("Credentials not available or invalid. Check your AWS credentials file.")


def upload_face_to_s3(file, patient_id: int) -> bool:
    return False
    try:
        picture = file.file
        picture.seek(
            0
        )  # Crucial step to move the file pointer to the beginning. If not, the file will be read as 0 bytes during the upload to S3.

        file_id = str(uuid.uuid4())
        _, file_extension = os.path.splitext(os.path.basename(file.name))

        object_key = f"{FOLDER_NAME}/{file_id}{file_extension}"
        extra_args = {"Metadata": {"patient_id": str(patient_id)}}

        s3.upload_fileobj(picture, BUCKET_NAME,
                          object_key, ExtraArgs=extra_args)

        print(
            f"File uploaded successfully. S3 location: {BUCKET_NAME}/{object_key}")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
