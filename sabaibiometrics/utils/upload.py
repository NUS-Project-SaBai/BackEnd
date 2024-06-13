import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"

BUCKET_NAME = "patients-images"
FOLDER_NAME = "index"
s3_client = None

try:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
except NoCredentialsError:
    print("Credentials not available or invalid. Check your AWS credentials file.")

def upload_face_to_s3(file, patient_id: int) -> bool:
    try:
        with file.open(mode="rb") as picture:
            s3_client.put_object(
                Body=picture,
                Bucket=BUCKET_NAME,
                Key=f"{FOLDER_NAME}/{patient_id}.jpeg",
                Metadata= {'id': str(patient_id)},
                ContentType='image/jpeg') 
        return True
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        return False
