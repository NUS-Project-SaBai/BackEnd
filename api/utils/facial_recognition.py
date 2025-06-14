import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from sabaibiometrics.settings import ENABLE_FACIAL_RECOGNITION

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "ap-southeast-1"
COLLECTION_ID = "sabai-test"

s3_client = None

try:
    rekognition_client = boto3.client(
        "rekognition",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
except NoCredentialsError:
    print("Credentials not available or invalid. Check your AWS credentials file.")


def generate_faceprint(file):
    """
    Uploads an image to AWS Rekognition API, returns the faceprint generated. Faceprint will be stored with
    patient details in database, under face encoding
    """

    if not ENABLE_FACIAL_RECOGNITION:
        return ""

    try:
        image_binary = getattr(file, "file").getvalue()

        response = rekognition_client.index_faces(
            CollectionId=COLLECTION_ID, Image={"Bytes": image_binary}, MaxFaces=3
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            # to find a better way to handle network errors here
            return ""

        # Gets faceprint of most prominent face
        faceprint = response["FaceRecords"][0]["Face"]["FaceId"]
        return faceprint

    except ClientError as e:
        print(f"Error indexing image: {e}")
        return ""
    except Exception as e:
        print(e)
        return ""


def search_faceprint(file):
    """
    Searches collection for faceprints that match the faces in image uploaded
    Returns a dictionary of {face_encoding: confidence} pairs
    Face_encoding is a hexadecimal string that identifies the patient
    """
    if not ENABLE_FACIAL_RECOGNITION:
        return {}

    try:
        image_binary = getattr(file, "file").getvalue()

        response = rekognition_client.search_faces_by_image(
            CollectionId=COLLECTION_ID, Image={"Bytes": image_binary}, MaxFaces=3
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            # to find a better way to handle network errors here
            return {}

        matched_faceprints = {}
        for match in response["FaceMatches"]:
            matched_faceprints[match["Face"]["FaceId"]] = match["Face"]["Confidence"]

        return matched_faceprints

    except ClientError as e:
        print(f"Error finding image, client error: {e}")
        return {}
