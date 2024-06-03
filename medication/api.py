import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from clinicmodels.models import Medication
from medication.forms import MedicationForm
from sabaibiometrics.serializers.medication_serializer import MedicationSerializer


"""
Handles all operations regarding the retrieval, update of medication models.
"""


class MedicationView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            medication_name = request.GET.get('name', '')
            medications = Medication.objects.all()

            if (medication_name):
                medications = medications.filter(
                    name__icontains=medication_name)
            response = serializers.serialize("json", medications)
            return HttpResponse(response, content_type='application/json')
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            medication = Medication.objects.get(pk=pk)
            response = serializers.serialize("json", [medication])
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def post(self, request):
        '''
        POST request with multipart form to create a new medication
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        '''
        try:
            form = MedicationForm(json.loads(request.body
                                             or None))
            if form.is_valid():
                medication = form.save()
                response = serializers.serialize("json", [medication, ])
                return HttpResponse(response, content_type="application/json")
            else:
                return JsonResponse(form.errors, status=400)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def patch(self, request, pk):
        '''
        PATCH request to update medication data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        '''
        try:
            medication = Medication.objects.get(pk=pk)

            quantityChange = request.data.get("quantityChange");

            data = {
                "quantity": medication.quantity + quantityChange
            }

            serializer = MedicationSerializer(medication, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return HttpResponse(json.dumps(serializer.data), content_type="application/json")

            else:
                return JsonResponse(serializer.errors, status=400)

        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except DataError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            medication = Medication.objects.get(pk=pk)
            medication.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
