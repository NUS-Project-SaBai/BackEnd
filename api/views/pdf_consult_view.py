from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from api.models.consult_model import Consult
from api.services.pdf_consult_service import generate_consult_pdf


class PdfConsultView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response({"error": "Consultation ID is required"}, status=404)

        consult = Consult.objects.filter(pk=pk).first()
        if consult is None:
            return Response({"error": "Consultation not found"}, status=404)

        buffer, filename = generate_consult_pdf(consult)

        return FileResponse(
            buffer,
            as_attachment=False,
            filename=filename,
            content_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
