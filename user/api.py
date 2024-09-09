from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
import json


class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            users = User.objects.all()
            response = serializers.serialize(
                "json", users, fields=['username'])
            return HttpResponse(response, content_type='application/json')
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            response = serializers.serialize(
                "json", [user], fields=['username'])
            return HttpResponse(response, content_type='application/json')
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=400)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist as e:
            return JsonResponse({"message": str(e)}, status=404)
            

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        if not (username):
            return JsonResponse({"status": "error", "errors": {"username": "This field is required."}}, status=400)
        
        user = User.objects.create(username=username)
        user.set_unusable_password()
        user.save()
        return JsonResponse({"user": {"id": user.id, "username": user.username, }}, status=201)