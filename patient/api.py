import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse

from clinicmodels.models import Patient
from patient.forms import PatientForm
from sabaibiometrics.serializers.patient_serializer import PatientSerializer
from sabaibiometrics.utils.upload import upload_face_to_s3
from sabaibiometrics.utils.search import search_face_with_rekognition
from sabaibiometrics.error_messages import NO_MATCH_FOUND, NO_IMAGE_FOUND

from rest_framework.views import APIView
from django.forms.models import model_to_dict

"""
Handles all operations regarding the retrieval, update of patient models.
"""


class PatientView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            patient_name = request.GET.get("name", "")

            patients = Patient.objects.all()

            if patient_name:
                patients = patients.filter(name__icontains=patient_name)
            responses = PatientSerializer(patients, many=True)
            return HttpResponse(
                json.dumps(responses.data), content_type="application/json"
            )
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            serializedPatient = PatientSerializer(patient)
            return HttpResponse(
                json.dumps(serializedPatient.data), content_type="application/json"
            )
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        """
        POST request with multipart form to create a new patient
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        """
        try:
            form = PatientForm(request.POST, request.FILES)
            if form.is_valid():
                patient = form.save()

                picture = request.FILES["picture"]

                upload_face_to_s3(picture, patient.id)

                response = json.dumps(PatientSerializer(patient).data)

                return HttpResponse(response, content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        """
        Update patient data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        """
        try:
            patient = Patient.objects.get(pk=pk)
            form = PatientForm(json.loads(request.body) or None, instance=patient)
            if form.is_valid():
                patient = form.save()
                response = serializers.serialize(
                    "json",
                    [
                        patient,
                    ],
                )
                return HttpResponse(response, content_type="application/json")

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            patient.picture.delete()
            patient.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)


class PatientSearchView(APIView):
    def post(self, request):
        try:
            image = request.FILES["picture"]
            response = search_face_with_rekognition(image)
            print(image.size)

            if "message" in response:
                return JsonResponse(response, status=404)

            patient = Patient.objects.get(id=int(response["patient_id"]))
            serializedPatient = PatientSerializer(patient)
            patientSearchResponse = {
                "patient": serializedPatient.data,
                "confidence": response["confidence"],
            }
            return HttpResponse(
                json.dumps(patientSearchResponse), content_type="application/json"
            )

        except Patient.DoesNotExist as e:
            return JsonResponse({"message": NO_MATCH_FOUND}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"message": NO_IMAGE_FOUND}, status=400)
