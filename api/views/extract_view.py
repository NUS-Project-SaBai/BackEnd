from rest_framework.views import APIView
from django.http import HttpResponse
from api.utils import extract_data_into_obj
from django.utils import timezone

class ExtractView(APIView):
    def get(self, request):
        # Call the function to get the Excel file in memory
        output = extract_data_into_obj()
        
        # Prepare the response
        response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f"attachment; filename=database_{timezone.now().strftime('%d%m%y_%H%M')}.xlsx"
        return response