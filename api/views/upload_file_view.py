from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import tempfile
from api.views import utils


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        labeled_filename = request.POST.get('file_name')

        if not uploaded_file:
            return JsonResponse({'error': 'No file was uploaded'}, status=400)

        if not labeled_filename:
            return JsonResponse({'error': 'No labeled filename provided'}, status=400)

        file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)

        # Save the file temporarily
        with open(file_path, 'wb+') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        # Call the function to upload to Google Drive
        utils.upload_photo(file_path, labeled_filename)

        # Optionally delete the temp file
        os.remove(file_path)

        return JsonResponse({'status': 'File uploaded successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)
