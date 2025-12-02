from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from api.models.consult_model import Consult
from api.services.pdf_consult_service import generate_multiple_consults_pdf


class PdfConsultView(APIView):
    def get(self, request, pk=None):
        patient_id = request.query_params.get("patient_id", None)
        if pk is None and patient_id is None:
            return Response({"error": "Consultation ID or Patient ID is required"}, status=404)


        if pk is not None:
            consult = [Consult.objects.filter(pk=pk).first()]
            patient = consult[0].visit.patient
            patient_pk = f"{patient.village_prefix}{patient.pk:04d}"
            filename = f"consultation{consult[0].id}_report_{patient_pk}.pdf"
        else:
            consult = Consult.objects.filter(visit__patient__id=patient_id).all()
            patient = consult[0].visit.patient
            patient_pk = f"{patient.village_prefix}{patient.pk:04d}"
            filename = f"consultation_report_{patient_pk}.pdf"
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
