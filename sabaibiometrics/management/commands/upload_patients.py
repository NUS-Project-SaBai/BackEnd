from django.core.management.base import BaseCommand
import psycopg2
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

class Command(BaseCommand):
    help = 'Extract patient data from old database and upload it to new database'

    def handle(self, *args, **kwargs):
        self.upload_data()

    def extract_data(self):
        db_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/past_data"
        engine = create_engine(db_url)
        query = "SELECT * FROM patients"
        data = pd.read_sql_query(query, con=engine)

        datetime_column = 'date_of_birth'
        if datetime_column in data.columns:
            data[datetime_column] = data[datetime_column].astype(str)

        engine.dispose()

        return data

    def get_current_columns(self):
        db_url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_NAME')}"
        engine = create_engine(db_url)
        
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('patients')]  

        engine.dispose()
        return columns
    
    def clean_data(self, data):
        current_columns = self.get_current_columns()
        data_cleaned = data.copy()

        columns_to_drop = [col for col in data_cleaned.columns if col not in current_columns]
        data_cleaned.drop(columns=columns_to_drop, inplace=True, errors='ignore')

        data_cleaned.fillna('', inplace=True)

        return data_cleaned

    def upload_data(self):
        data = self.extract_data()
        cleaned_data = self.clean_data(data)
        json_data = cleaned_data.to_dict(orient='records')
        response = requests.post('http://localhost:8000/upload_patient', json=json_data)
        if response.status_code in [200, 201]:
            self.stdout.write(f"Patient data uploaded successfully: {response.text}")
        else:
            self.stdout.write(f"Failed to upload patient data: {response.status_code} {response.text}")