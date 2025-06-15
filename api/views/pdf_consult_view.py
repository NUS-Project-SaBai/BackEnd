import io

from django.http import FileResponse
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Frame, PageTemplate, Paragraph, SimpleDocTemplate
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.consult_model import Consult
from api.models.diagnosis_model import Diagnosis

styles = getSampleStyleSheet()
_baseFontName = "Helvetica"
_baseFontNameB = "Helvetica-Bold"
title_style = ParagraphStyle(
    name="Title",
    fontName=_baseFontNameB,
    fontSize=16,
    alignment=TA_CENTER,
)
heading1_style = ParagraphStyle(
    name="Heading1",
    fontName=_baseFontNameB,
    fontSize=16,
    leading=16,
    spaceBefore=20,
    spaceAfter=14,
)
heading2_style = ParagraphStyle(
    name="Heading2",
    fontName=_baseFontNameB,
    fontSize=12,
    spaceBefore=8,
    leading=16,
)
normal_style = ParagraphStyle(
    name="Normal",
    fontName=_baseFontName,
    fontSize=12,
    leading=14,
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    leftIndent=6,
)


class PdfConsultView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response({"error": "Consultation ID is required"}, status=404)
        consult = Consult.objects.filter(pk=pk).first()
        if consult is None:
            return Response({"error": "Consultation not found"}, status=404)
        patient = consult.visit.patient
        patient_id = f"{patient.village_prefix}{patient.pk:04d}"
        diagnosis = Diagnosis.objects.filter(consult=consult)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        flowables = []

        def draw_section(
            title,
            body="",
            title_style=heading1_style,
        ):
            flowables.append(Paragraph(title, style=title_style))
            for line in body.splitlines():
                flowables.append(Paragraph(line, style=normal_style))

        draw_section("Consultation Report - " + patient_id, title_style=title_style)
        draw_section("Patient Name:", patient.name or "N/A")
        draw_section("Past Medical History", consult.past_medical_history or "N/A")
        draw_section("Consultation", consult.consultation or "N/A")
        draw_section(
            "Diagnosis",
        )  # heading for diagnosis section
        for diag in diagnosis:
            draw_section(
                diag.category, diag.details or "N/A", title_style=heading2_style
            )
        draw_section("Plan", consult.plan or "N/A")
        draw_section("Referred For:", consult.referred_for or "N/A")
        draw_section("Referral Notes", consult.referral_notes or "N/A")
        draw_section("Remarks", consult.remarks or "N/A")

        def header(canvas: canvas.Canvas, doc: SimpleDocTemplate):
            canvas.saveState()
            canvas.setTitle(f"Consultation Report - {patient_id}")
            canvas.setFont("Helvetica", 10)

            canvas.drawString(
                doc.width + doc.leftMargin,
                doc.height + doc.bottomMargin + doc.topMargin - 30,
                patient_id,
            )
            canvas.drawString(
                doc.width + doc.leftMargin,
                doc.height + doc.bottomMargin + doc.topMargin - 50,
                str(doc.page),
            )
            canvas.restoreState()

        page_t = PageTemplate(
            id="header",
            frames=Frame(
                doc.leftMargin,
                doc.bottomMargin,
                doc.width,
                doc.height,
                id="normal",
            ),
            onPage=header,
        )
        doc.addPageTemplates([page_t])
        doc.build(flowables, onFirstPage=header, onLaterPages=header)
        buffer.seek(0)
        filename = f"consultation{consult.pk}_report_{patient_id}.pdf"
        return FileResponse(
            buffer,
            as_attachment=False,
            filename=filename,
            content_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
            },
        )
