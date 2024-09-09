from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from clinicmodels.models import Visit, PostReferral
from postreferral.forms import PostreferralForm


@api_view(['POST'])
@csrf_exempt
def create_new_postreferral(request):
    try:
        if 'visit' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'visit' not found"}, status=400)
        visit = request.POST['visit']

        Visit.objects.get(pk=visit)
        postreferral_form = PostreferralForm(request.POST)
        if postreferral_form.is_valid():
            postreferral = postreferral_form.save()
            response = serializers.serialize("json", [postreferral, ])
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse(postreferral_form.errors, status=400)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['POST'])
@csrf_exempt
def update_postreferral(request):
    try:
        if 'id' not in request.POST:
            return JsonResponse({"message": "POST: parameter 'id' not found"}, status=400)
        postreferral_id = request.POST['id']
        postreferral = PostReferral.objects.get(pk=postreferral_id)
        if 'recorder' in request.POST:
            postreferral.recorder = request.POST['recorder']
        if 'remarks' in request.POST:
            postreferral.remarks = request.POST['remarks']
        postreferral.save()
        response = serializers.serialize("json", [postreferral, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_postreferral_by_id(request):
    try:
        if 'id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'id' not found"}, status=400)
        postreferral_id = request.GET['id']
        postreferral = PostReferral.objects.get(pk=postreferral_id)
        response = serializers.serialize("json", [postreferral, ])
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_postreferral_by_visit(request):
    try:
        if 'visit_id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'visit_id' not found"}, status=400)
        visit_id = request.GET['visit_id']
        postreferral = PostReferral.objects.filter(visit=visit_id)
        response = serializers.serialize("json", postreferral)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)


@api_view(['GET'])
def get_postreferral_by_patient(request):
    try:
        if 'patient_id' not in request.GET:
            return JsonResponse({"message": "GET: parameter 'patient_id' not found"}, status=400)
        patient_id = request.GET['patient_id']
        postreferral = PostReferral.objects.filter(visit__patient_id=patient_id)
        response = serializers.serialize("json", postreferral)
        return HttpResponse(response, content_type='application/json')
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": str(e)}, status=404)
    except DataError as e:
        return JsonResponse({"message": str(e)}, status=400)
