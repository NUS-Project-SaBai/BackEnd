from rest_framework.views import APIView
from django.http import FileResponse
from api.services.pdf_consult_service import generate_all_patients_pdfs_zip


class PdfAllReportView(APIView):
    """
    API endpoint to generate PDF reports for all patients with consultations
    and return them as a single zip file.
    """
    
    def get(self, request):
        """
        Generate a zip file containing PDF consultation reports for all patients.
        
        Returns:
            FileResponse: A zip file containing individual patient PDF reports.
        """
        zip_buffer, zip_filename = generate_all_patients_pdfs_zip()
        
        return FileResponse(
            zip_buffer,
            as_attachment=True,
            filename=zip_filename,
            content_type="application/zip",
        )
