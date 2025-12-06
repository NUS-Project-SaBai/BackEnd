import datetime
import io
import zipfile
from typing import Iterable, Tuple

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Frame,
    PageTemplate,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    HRFlowable,
)
from reportlab.pdfgen import canvas

from api.models import Diagnosis, Consult
from api.models.patient_model import Patient
import csv


def _build_styles():
    """Return a dict of ParagraphStyle objects used by the PDF generator."""
    base = "Helvetica"
    bold = "Helvetica-Bold"
    return {
        "title": ParagraphStyle(
            name="Title",
            fontName=bold,
            fontSize=18,
            alignment=TA_CENTER,
            spaceBefore=12,
            spaceAfter=20,
        ),
        "consultation_header": ParagraphStyle(
            name="ConsultationHeader",
            fontName=bold,
            fontSize=15,
            leading=18,
            spaceBefore=20,
            spaceAfter=12,
            textColor="#1a4d8f",
        ),
        "h1": ParagraphStyle(
            name="Heading1",
            fontName=bold,
            fontSize=13,
            leading=16,
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            name="Heading2",
            fontName=bold,
            fontSize=11,
            spaceBefore=10,
            spaceAfter=6,
            leading=14,
        ),
        "normal": ParagraphStyle(
            name="Normal",
            fontName=base,
            fontSize=10,
            leading=14,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leftIndent=12,
        ),
    }


def _draw_section(
    flowables: list, title: str, body: str = "", style: ParagraphStyle = None
):
    """Append title and body paragraphs to the flowables list using provided style."""
    if style is None:
        # fall back to a simple style; caller should normally pass one
        style = _build_styles()["h1"]
    flowables.append(Paragraph(title, style=style))
    if body:
        for line in str(body).splitlines():
            flowables.append(Paragraph(line, style=_build_styles()["normal"]))


def _header_factory(patient_id: str):
    """Return a header function bound to a patient_id for use with `onPage`."""

    def header(c: canvas.Canvas, doc: SimpleDocTemplate):
        c.saveState()
        c.setTitle(f"Consultation Report - {patient_id}")
        c.setFont("Helvetica", 10)
        # Draw patient id
        x = doc.leftMargin + doc.width
        y1 = doc.bottomMargin + doc.topMargin + doc.height - 30
        y2 = y1 - 20
        c.drawString(x, y1, patient_id)
        c.restoreState()

    return header


def _footer_factory():
    """Return a footer function that draws page number at bottom-right."""

    def footer(c: canvas.Canvas, doc: SimpleDocTemplate):
        c.saveState()
        c.setFont("Helvetica", 9)
        x = doc.leftMargin + doc.width
        y = doc.bottomMargin + 10
        # drawRightString places the end of the text at x, which aligns to bottom-right
        try:
            c.drawRightString(x, y, f"Page {getattr(doc, 'page', '')}")
        except Exception:
            # fallback if drawRightString is unavailable
            c.drawString(x, y, str(getattr(doc, "page", "")))
        c.restoreState()

    return footer


def generate_single_consult_pdf(consult, title=None) -> Tuple[io.BytesIO, str]:
    """Generate a PDF for a single consult.

    Convenience wrapper around `generate_multiple_consults_pdf` that sets the
    filename based on the consult and patient.
    """
    patient = consult.visit.patient
    filename = f"consultation{consult.id}_report_{patient.pk}.pdf"
    return generate_multiple_consults_pdf([consult], patient, filename=filename)


def generate_multiple_consults_pdf(
    consults: Iterable, patient: Patient, filename: str = None, title: str = None
) -> Tuple[io.BytesIO, str]:
    """Generate a PDF buffer and filename for multiple consults for a patient.

    Returns (buffer, filename). If `filename` is omitted a default name is used.
    """
    styles = _build_styles()
    patient_id = f"{patient.village_prefix}{patient.pk:04d}"
    if not filename:
        filename = f"consult_report_{patient_id}.pdf"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    flowables = []

    # Content sections
    _draw_section(
        flowables, title or f"Consultation Report - {patient_id}", style=styles["title"]
    )
    _draw_section(flowables, "Patient Name:", patient.name or "N/A", style=styles["h1"])

    # Add separator after patient info
    flowables.append(
        HRFlowable(
            width="100%", thickness=2, color="#1a4d8f", spaceBefore=10, spaceAfter=15
        )
    )

    for idx, consult in enumerate(consults):
        # Add separator between consultations (not before the first one)
        if idx > 0:
            flowables.append(Spacer(1, 0.3))
            flowables.append(
                HRFlowable(
                    width="100%",
                    thickness=1.5,
                    color="#cccccc",
                    spaceBefore=5,
                    spaceAfter=10,
                )
            )
            flowables.append(Spacer(1, 0.2))

        diagnoses = Diagnosis.objects.filter(consult=consult)
        _draw_section(
            flowables,
            "Consultation Date: " + consult.date.strftime("%Y-%m-%d"),
            style=styles["consultation_header"],
        )

        _draw_section(
            flowables,
            "Past Medical History",
            consult.past_medical_history or "N/A",
            style=styles["h2"],
        )

        _draw_section(
            flowables,
            "Consultation",
            consult.consultation or "N/A",
            style=styles["h2"],
        )

        _draw_section(flowables, "Diagnosis", style=styles["h1"])
        for diag in diagnoses:
            _draw_section(
                flowables,
                diag.category or "",
                diag.details or "N/A",
                style=styles["h2"],
            )

        flowables.append(Spacer(1, 0.1 * inch))
        _draw_section(flowables, "Plan", consult.plan or "N/A", style=styles["h2"])

        if consult.referred_for:
            _draw_section(
                flowables,
                "Referred For:",
                consult.referred_for,
                style=styles["h2"],
            )
            _draw_section(
                flowables,
                "Referral Notes",
                consult.referral_notes,
                style=styles["h2"],
            )

        _draw_section(
            flowables, "Remarks", consult.remarks or "N/A", style=styles["h2"]
        )

    # Header and page template
    header = _header_factory(patient_id)
    footer = _footer_factory()

    def _on_page(c: canvas.Canvas, d: SimpleDocTemplate):
        # call header and footer on each page
        header(c, d)
        footer(c, d)

    page_template = PageTemplate(
        id="header",
        frames=Frame(
            doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
        ),
        onPage=_on_page,
    )
    doc.addPageTemplates([page_template])
    doc.build(flowables, onFirstPage=_on_page, onLaterPages=_on_page)

    buffer.seek(0)
    return buffer, filename


def generate_all_patients_pdfs_zip() -> Tuple[io.BytesIO, str]:
    """Generate PDFs for all patients with consultations and zip them.

    Returns (zip_buffer, filename) containing individual patient consultation reports.
    Only includes patients that have at least one consultation.
    """
    # Get all patients who have consultations
    patients_with_consults = (
        Patient.objects.filter(to_get_report=True, visit__consult__isnull=False)
        .distinct()
        .order_by("pk")
    )

    zip_buffer = io.BytesIO()
    zip_filename = (
        f"all_patient_reports_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    )
    print(f"Generating reports for {patients_with_consults.count()} patients.")

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for patient in patients_with_consults:
            # Get all consults for this patient
            consults = (
                Consult.objects.filter(visit__patient=patient)
                .select_related("visit")
                .order_by("date")
            )
            print(consults.values())

            if consults.exists():
                # Generate PDF for this patient
                patient_id = f"{patient.village_prefix}{patient.pk:04d}"
                filename = f"consult_report_{patient_id}.pdf"

                try:
                    pdf_buffer, _ = generate_multiple_consults_pdf(
                        consults, patient, filename=filename
                    )

                    # Add PDF to zip file
                    zip_file.writestr(filename, pdf_buffer.getvalue())
                except Exception as e:
                    # Log error but continue with other patients
                    print(f"Error generating PDF for patient {patient_id}: {str(e)}")
                    continue

        # Generate a csv file for them to view the patient id and their contact number
        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["Patient ID", "Contact Number"])
        for patient in patients_with_consults:
            patient_id = f"{patient.village_prefix}{patient.pk:04d}"
            contact_number = patient.contact_no or "N/A"
            csv_writer.writerow([patient_id, contact_number])
        csv_filename = "patient_contact_numbers.csv"
        zip_file.writestr(csv_filename, csv_buffer.getvalue())

    zip_buffer.seek(0)
    return zip_buffer, zip_filename
