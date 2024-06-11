from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from api.serializers import UserSerializer
import json

class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def get_object(self, pk):
        try:
            users = User.objects.get(pk=pk)
            serializer = UserSerializer(users)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "Deleted successfully"})
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=500)
