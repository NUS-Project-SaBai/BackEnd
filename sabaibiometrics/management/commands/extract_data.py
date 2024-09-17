import os
import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Patient, Visit, Vitals, Consult, Diagnosis, Medication, Order, CustomUser, MedicationReview

class Command(BaseCommand):
    help = 'Extract data from Django models and save to Excel with multiple sheets'

    def handle(self, *args, **kwargs):
        # Define the models and their corresponding sheet names
        models = {
            'patients': Patient,
            'clinics': Visit,
            'medicines': Vitals,
            'appointments': Consult,
            'diagnoses': Diagnosis,
            'medication': Medication, 
            'order': Order,
            'customUser': CustomUser, 
            'medicationReview': MedicationReview
        }

        # Directory where CSV files will be temporarily saved
        temp_csv_dir = 'temp_csv'
        os.makedirs(temp_csv_dir, exist_ok=True)

        # Save each model's data to a separate CSV file
        for table_name, model in models.items():
            queryset = model.objects.all().values()
            df = pd.DataFrame(list(queryset))
            csv_filename = os.path.join(temp_csv_dir, f"{table_name}.csv")
            df.to_csv(csv_filename, index=False)
            self.stdout.write(self.style.SUCCESS(f'Data from table {table_name} exported to {csv_filename}.'))

        # Create a list to store dataframes and their sheet names
        dataframes = []
        
        # Read each CSV file and store it as a dataframe in the list
        for filename in os.listdir(temp_csv_dir):
            if filename.endswith('.csv'):
                file_path = os.path.join(temp_csv_dir, filename)
                sheet_name = os.path.splitext(filename)[0]  # Use filename (without extension) as sheet name
                df = pd.read_csv(file_path)
                dataframes.append((sheet_name, df))

        # Save all dataframes to an Excel file with multiple sheets
        excel_filename = 'final_data.xlsx'
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            for sheet_name, df in dataframes:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f'CSV files have been combined into {excel_filename}.')
        print(f'CSV files are available in the {temp_csv_dir} directory.')
        
        # Clean up the temporary CSV directory
        for file in os.listdir(temp_csv_dir):
            file_path = os.path.join(temp_csv_dir, file)
            os.remove(file_path)
        os.rmdir(temp_csv_dir)
        
        print(f'Temporary CSV files have been cleaned up.')
