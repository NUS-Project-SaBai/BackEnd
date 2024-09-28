from django.core.management.base import BaseCommand
import pandas as pd
import certifi
import ssl
import urllib.request
from api.models import Medication

class Command(BaseCommand):
  help = 'Update stock from google sheets'

  def handle(self, *args, **kwargs):
        # SSL Security Stuff
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context)))

        sheet_id = '1qsFXBcIw4SUfvdSHFKv7hg0sYAOuf5pW8lhcw8-N5DM'

        # Fetch and print the data for now
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df = pd.read_csv(url)
            print(df)

            for index, row in df.iterrows():
                medicine_name=row['Drug (A-Z)']
                quantity = row['End Dec 2023 Qty']
                notes = ''

                medication, created = Medication.objects.update_or_create(
                    medicine_name=medicine_name,
                    defaults={
                        'quantity': quantity if pd.notna(quantity) else 0,
                        'notes': notes if pd.notna(notes) else ''
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created {medicine_name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated {medicine_name}"))

        except Exception as e:
            self.stderr.write(f"Couldn't read csv: {e}")