from django.core.management.base import BaseCommand
from api import utils
from django.utils import timezone

class Command(BaseCommand):
    help = 'Extract data from Django models and save to Excel with multiple sheets'

    def handle(self, *args, **kwargs):
        output = utils.extract_data_into_obj()
        excel_filename = f"database_{timezone.now().strftime('%d%m%y_%H%M')}.xlsx"

        # Save the BytesIO stream to a local file
        with open(excel_filename, 'wb') as f:
            f.write(output.getvalue())

        self.stdout.write(self.style.SUCCESS(f'Successfully extracted data and saved to {excel_filename}.'))