from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models.consult_model import Consult
from api.services.pdf_consult_service import generate_multiple_consults_pdf


class PdfConsultView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            return Response({"error": "Consultation ID or Patient ID is required"}, status=404)

        consult = [Consult.objects.filter(pk=pk).first()]
        patient = consult[0].visit.patient
        patient_pk = f"{patient.village_prefix}{patient.pk:04d}"
        filename = f"consultation{consult[0].id}_report_{patient_pk}.pdf"
        if len(consult) == 0:
            return Response({"error": "Consultation(s) not found"}, status=404)

        buffer, filename = generate_multiple_consults_pdf(consult, patient, filename=filename)

        return FileResponse(
            buffer,
            as_attachment=False,
            filename=filename,
            content_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )
