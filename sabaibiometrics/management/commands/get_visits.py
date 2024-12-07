from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from api.models import Visit
from django.db.utils import IntegrityError
import requests
from sabaibiometrics.settings import CLOUDINARY_URL
from django.conf import settings
import os
import psycopg2
from django.utils import timezone
import datetime


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
            query = "SELECT * FROM visits;"

            # Execute the query
            cursor.execute(query)

            # Fetch all rows from the result of the query
            rows = cursor.fetchall()

            # The rows variable now contains a 2D list, where each row is represented by a list
            # You can print it, process it, or return it as needed
            print(rows)  # Or return rows if needed

            for row in rows:
                visit = Visit.objects.create(
                    id=row[0],
                    date=row[1],
                    status=row[2],
                    patient_id=row[3],
                )

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()