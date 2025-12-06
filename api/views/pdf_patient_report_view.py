import io
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from api.models.consult_model import Consult
from api.models.patient_model import Patient
from api.services.pdf_consult_service import (
    generate_multiple_consults_pdf,
    generate_single_consult_pdf,
)


class PdfPatientReportView(APIView):
    """
    API view to generate and return the latest PDF report for a specific patient.
    """

    def get(self, request, patient_id, report_type):
        if report_type is None or patient_id is None:
            return Response(
                {"error": "Patient ID and report type are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        patient = Patient.objects.filter(pk=patient_id).first()
        if not patient:
            return Response(
                {"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND
            )
        if report_type == "latest_consult":
            return self._get_latest_consult(patient.id)
        elif report_type == "all_consults":
            return self._get_all_consults(patient)
        else:
            return Response(
                {
                    "error": "Invalid report type. Use 'latest_consult' or 'all_consult'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def _get_latest_consult(self, patient_id: int):
        """
        Helper method to retrieve the latest consult for a given patient.
        """
        latest_consult = (
            Consult.objects.filter(visit__patient__id=patient_id)
            .order_by("-date")
            .first()
        )
        if not latest_consult:
            return Response(
                {"error": "No consults found for this patient."},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            patient = latest_consult.visit.patient

        buffer, filename = generate_single_consult_pdf(latest_consult)
        return self._convert_to_pdf_file_response(buffer, filename)

    def _get_all_consults(self, patient: Patient):
        """
        Helper method to retrieve all consults for a given patient.
        """
        consults = (
            Consult.objects.filter(visit__patient=patient)
            .select_related("visit")
            .order_by("date")
        )

        if not consults.exists():
            return Response(
                {"error": "No consults found for this patient."},
                status=status.HTTP_404_NOT_FOUND,
            )

        patient_pk = f"{patient.village_prefix}{patient.pk:04d}"
        filename = f"{patient_pk}_consultation_report.pdf"

        buffer, filename = generate_multiple_consults_pdf(consults, patient, filename)

        return self._convert_to_pdf_file_response(buffer, filename)

    def _convert_to_pdf_file_response(
        self, buffer: io.BytesIO, filename: str
    ) -> FileResponse:
        """
        Helper method to convert a BytesIO buffer to a Django FileResponse.
        """
        return FileResponse(
            buffer,
            as_attachment=False,
            filename=filename,
            content_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
