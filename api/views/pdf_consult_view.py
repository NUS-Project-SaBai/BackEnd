import io

from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
        width, height = A4
        y = height - 50

        def draw_section(title, body, bold=True, space_after=20):
            nonlocal y
            if bold:
                p.setFont("Helvetica-Bold", 12)
            else:
                p.setFont("Helvetica", 12)
            p.drawString(40, y, title)
            y -= 18
            p.setFont("Helvetica", 11)
            for line in body.splitlines():
                p.drawString(50, y, line.strip())
                y -= 16
            y -= space_after

        # Optional top ID (like <<TT0057>>)
        draw_section("<<TT0057>>", "", bold=False, space_after=12)

        draw_section("Patient Name:", consult.patient_name or "N/A")
        draw_section("Past Medical History", consult.medical_history or "N/A")
        draw_section("Consultation", consult.consultation or "N/A")

        draw_section("Diagnosis", "")  # heading for diagnosis section
        if hasattr(consult, "diagnoses") and consult.diagnoses.exists():
            for diag in consult.diagnoses.all():
                draw_section(f"<{diag.category}>", diag.body or "N/A", space_after=10)
        else:
            draw_section("<Diagnosis Category>", "<Diagnosis body/details>", space_after=10)
            draw_section("<Diagnosis 2 Category>", "<Diagnosis 2 body/details>", space_after=10)

        draw_section("Plan", consult.plan or "N/A")
        draw_section("Referred For:", consult.referred_for or "N/A")
        draw_section("Referral Notes", consult.referral_notes or "N/A")
        draw_section("Remarks", consult.remarks or "N/A")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=False, filename=f"consultation_report_{pk}.pdf"
        )
