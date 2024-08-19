from django.core.management.base import BaseCommand
import pandas as pd
import certifi
import ssl
import urllib.request
class Command(BaseCommand):
  help = 'Update stock from google sheets'

  def handle(self, *args, **kwargs):
        # SSL Security Stuff
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        urllib.request.install_opener(urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context)))

        sheet_id = '1qsFXBcIw4SUfvdSHFKv7hg0sYAOuf5pW8lhcw8-N5DM' #to move to .env soon

        # Fetch and print the data for now
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df = pd.read_csv(url)
            print(df)
        except Exception as e:
            self.stderr.write(f"Couldn't read csv: {e}")