import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Frame,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
)

from api.models import Diagnosis
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("KhmerFont", "./NotoSansKhmer-VariableFont.ttf"))
pdfmetrics.registerFont(TTFont("KhmerFont-Bold", "./NotoSansKhmer-Bold.ttf"))

def generate_consult_pdf(consult):
    doctor = consult.doctor
    patient = consult.visit.patient
    patient_id = f"{patient.village_prefix}{patient.pk:04d}"
    diagnosis = Diagnosis.objects.filter(consult=consult)

    # Setup PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    flowables = []

    # --- Styles ---
    _baseFontName = "KhmerFont"
    _baseFontNameB = "KhmerFont-Bold"
    title_style = ParagraphStyle(
        name="Title", fontName=_baseFontNameB, fontSize=16, alignment=TA_CENTER
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
        name="Heading2", fontName=_baseFontNameB, fontSize=12, spaceBefore=8, leading=16
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

    # --- Draw helper ---
    def draw_section(title, body="", title_style=heading1_style):
        flowables.append(Paragraph(title, style=title_style))
        for line in body.splitlines():
            flowables.append(Paragraph(line, style=normal_style))

    # --- Content ---
    draw_section("Consultation Report - " + patient_id, title_style=title_style)
    draw_section("Doctor Name:", doctor.nickname or "N/A")
    draw_section("Patient Name:", patient.name or "N/A")
    draw_section("Past Medical History", consult.past_medical_history or "N/A")
    draw_section("Consultation", consult.consultation or "N/A")
    draw_section("Diagnosis")
    for diag in diagnosis:
        draw_section(diag.category, diag.details or "N/A", title_style=heading2_style)
    draw_section("Plan", consult.plan or "N/A")
    draw_section("Referred For:", consult.referred_for or "N/A")
    draw_section("Referral Notes", consult.referral_notes or "N/A")
    draw_section("Remarks", consult.remarks or "N/A")

    # --- Header ---
    def header(c: canvas.Canvas, doc: SimpleDocTemplate):
        c.saveState()
        c.setTitle(f"Consultation Report - {patient_id}")
        c.setFont("Helvetica", 10)
        c.drawString(
            doc.width + doc.leftMargin,
            doc.height + doc.bottomMargin + doc.topMargin - 30,
            patient_id,
        )
        c.drawString(
            doc.width + doc.leftMargin,
            doc.height + doc.bottomMargin + doc.topMargin - 50,
            str(doc.page),
        )
        c.restoreState()

    page_template = PageTemplate(
        id="header",
        frames=Frame(
            doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
        ),
        onPage=header,
    )
    doc.addPageTemplates([page_template])
    doc.build(flowables, onFirstPage=header, onLaterPages=header)

    buffer.seek(0)
    filename = f"consultation{consult.pk}_report_{patient_id}.pdf"
    return buffer, filename
