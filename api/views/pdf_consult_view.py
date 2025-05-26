import io

from django.http import FileResponse
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.consult_model import Consult


class PdfConsultView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response({"error": "Consultation ID is required"}, status=404)
        consult = Consult.objects.filter(pk=pk).first()
        if consult is None:
            return Response({"error": "Consultation not found"}, status=404)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize="A4")
        p.setTitle(f"Consultation Report for Consult ID: {pk}")
        p.drawString(
            20,
            700,
            f"Consultation Report for Consult ID: {pk}",
            mode=0,
            charSpace=1,
            wordSpace=1,
        )
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=False, filename=f"consultation_report_{pk}.pdf"
        )
