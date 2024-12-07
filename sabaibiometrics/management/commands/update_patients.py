from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Patient
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
from django.conf import settings
import os
import psycopg2
from django.utils import timezone
import datetime
from api.utils import facial_recognition
from django.core.files import File
from io import BytesIO
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

COLLECTION_ID = "sabai-test"

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


class Command(BaseCommand):
    help = "Get image from cloudinary to offline"

    def handle(self, *args, **kwargs):
        settings.DATABASES["old_sabai_data"] = {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "old_sabai_data",
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }

        # Get the database settings from Django settings
        db_settings = settings.DATABASES["old_sabai_data"]

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_settings["NAME"],
            user=db_settings["USER"],
            password=db_settings["PASSWORD"],
            host=db_settings["HOST"],
            port=db_settings["PORT"]
        )

        try:
            # Create a cursor to execute the query
            cursor = conn.cursor()

            # Define the SQL query to fetch all rows from the "patients" table
            query = "SELECT * FROM patients;"

            # Execute the query
            cursor.execute(query)

            # Fetch all rows from the result of the query
            rows = cursor.fetchall()

            # The rows variable now contains a 2D list, where each row is represented by a list
            # You can print it, process it, or return it as needed
            print(rows)  # Or return rows if needed

            for row in rows:
                patient = Patient.objects.filter(id=row[0]).first()
                filename = "media/offline_pictures/" + row[11].split('/')[-1]

                # Open the file in binary mode
                with open(filename, "rb") as image_file:
                    file_content = BytesIO(image_file.read())

                    # Pass the BytesIO object to generate_faceprint
                    patient.face_encodings = generate_faceprint(file_content)
                    patient.save()
                    print("saved", row)

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

def generate_faceprint(file):
    '''
    Uploads an image to AWS Rekognition API, returns the faceprint generated. Faceprint will be stored with
    patient details in database, under face encoding
    '''

    # Use getvalue() directly on the BytesIO object
    image_binary = file.getvalue()

    response = rekognition_client.index_faces(
        CollectionId=COLLECTION_ID,
        Image={
            'Bytes': image_binary
        },
        MaxFaces=3
    )

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        # to find a better way to handle network errors here
        return ''

    # Gets faceprint of most prominent face
    faceprint = response['FaceRecords'][0]['Face']['FaceId']
    return faceprint