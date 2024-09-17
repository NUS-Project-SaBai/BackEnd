from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db import IntegrityError, ProgrammingError
from datetime import datetime
import os
from collections import defaultdict, deque


class Command(BaseCommand):
    help = "Export all data from all models to a timestamped SQLite database"

    def get_model_dependencies(self):
        """
        Returns a sorted list of models respecting their foreign key dependencies.
        """
        models = apps.get_models()
        order = ['Group', 'ContentType', 'Permission', 'LogEntry', 'Patient', 'File', 'Visit', 'CustomUser', 'Consult',
                 'Diagnosis', 'Medication', 'MedicationReview', 'Order']
        model_order_map = {name: index for index, name in enumerate(order)}
        sorted_models = sorted(models, key=lambda model: model_order_map.get(
            model.__name__, float('inf')))

        for model in sorted_models:
            print(model.__name__)

        return sorted_models

    def handle(self, *args, **kwargs):
        # Create a timestamp for the new SQLite file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sqlite_db_filename = f'db_{timestamp}.sqlite3'
        sqlite_db_path = os.path.join(os.getcwd(), sqlite_db_filename)

        self.stdout.write(self.style.SUCCESS(
            f'Creating new SQLite database at {sqlite_db_filename}...'))

        # Update the 'sqlite' database path dynamically
        settings.DATABASES['sqlite']['NAME'] = sqlite_db_path

        # Run migrations for the SQLite database
        call_command('migrate', database='sqlite')

        # Get all models registered in the Django project
        sorted_models = self.get_model_dependencies()

        # Loop over all models and export their data to the SQLite database
        for model in sorted_models:
            try:
                self.stdout.write(
                    f"Exporting data for model: {model.__name__}...")
                objects = model.objects.all()

                for obj in objects:
                    try:
                        # Save the object using the 'sqlite' database
                        obj.save(using='sqlite')
                    except IntegrityError as e:
                        self.stdout.write(f"IntegrityError: {e}")
                    except Exception as e:
                        self.stdout.write(f"Unhandled exception: {e}")

            except ProgrammingError as e:
                self.stdout.write(f"Skipping model {model.__name__}: {e}")

        self.stdout.write(self.style.SUCCESS(
            f'Data export completed. Database created at: {sqlite_db_filename}'))
