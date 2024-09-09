import boto3
from botocore.exceptions import NoCredentialsError
from typing import IO, List
from PIL import Image
# from sabaibiometrics.settings import (
#     AWS_SECRET_ACCESS_KEY,
#     AWS_ACCESS_KEY_ID,
#     AWS_REGION,
# )
from sabaibiometrics.error_messages import NO_MATCH_FOUND


# rekognition, dynamodb = None, None

# try:
#     rekognition = boto3.client(
#         "rekognition",
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         region_name=AWS_REGION,
#     )

#     dynamodb = boto3.client(
#         "dynamodb",
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#         region_name=AWS_REGION,
#     )
# except NoCredentialsError:
#     print("Credentials not available or invalid. Check your AWS credentials file.")


def search_face_with_rekognition(image: IO) -> List:
    return {
        "patient_id": None,
        "confidence": None

    }
    image_binary = image.read()

    response = rekognition.search_faces_by_image(
        CollectionId="projectsabai", Image={"Bytes": image_binary}
    )
    if len(response["FaceMatches"]) == 0:
        return {
            "message": NO_MATCH_FOUND,
        }

    matched_patient = response["FaceMatches"][0]["Face"]

    face = dynamodb.get_item(
        TableName="projectsabai",
        Key={"RekognitionId": {"S": matched_patient["FaceId"]}},
    )

    print(face)

    if "Item" not in face:
        return {
            "message": NO_MATCH_FOUND,
        }

    return {
        "patient_id": face["Item"]["PatientId"]["S"],
        "confidence": matched_patient["Confidence"],
    }
