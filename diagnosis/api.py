import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from clinicmodels.models import Consult, Diagnosis
from diagnosis.forms import DiagnosisForm
from sabaibiometrics.serializers.diagnosis_serializer import DiagnosisSerializer


class DiagnosisView(APIView):
    def get(self, request, pk=None):
        pk = request.query_params.get("consult")
        if pk is not None:
            return self.get_object(pk)
        try:
            diagnosises = Diagnosis.objects.all()

            serializer = DiagnosisSerializer(diagnosises, many=True)
            return HttpResponse(
                json.dumps(serializer.data), content_type="application/json"
            )
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            diagnosis = Diagnosis.objects.filter(consult=pk)
            print(diagnosis)
            serializer = DiagnosisSerializer(diagnosis, many=True)
            return HttpResponse(
                json.dumps(serializer.data), content_type="application/json"
            )
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        """
        POST request with multipart form to create a new diagnosis
        :param request: POST request with the required parameters.
        :return: Http Response with corresponding status code
        """
        try:
            data = json.loads(request.body) or None
            if "consult" not in data:
                return JsonResponse(
                    {"message": "POST: parameter 'consult' not found"}, status=400
                )
            consult_id = data["consult"]
            Consult.objects.get(pk=consult_id)

            diagnosis_form = DiagnosisForm(data)
            if diagnosis_form.is_valid():
                consult = diagnosis_form.save()
                serializer = DiagnosisSerializer(consult)
                return HttpResponse(
                    json.dumps(serializer.data), content_type="application/json"
                )
            else:
                return JsonResponse({"message": diagnosis_form.errors}, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=405)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def put(self, request, pk):
        """
        Update consult data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        """
        try:
            consult = Consult.objects.get(pk=pk)
            form = DiagnosisForm(json.loads(request.body)
                               or None, instance=consult)
            if form.is_valid():
                consult = form.save()
                serializer = DiagnosisSerializer(consult)
                return HttpResponse(
                    json.dumps(serializer.data), content_type="application/json"
                )

            else:
                return JsonResponse(form.errors, status=400)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            consult = Consult.objects.get(pk=pk)
            consult.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
