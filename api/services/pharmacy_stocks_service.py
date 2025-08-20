from api.models import Medication
from collections import defaultdict


def get_pharmacy_stock_viewmodel():
    medication_data = Medication.objects.all().values('id', 'medicine_name', 'quantity', 'code')
    return list(medication_data)
