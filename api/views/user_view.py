from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from api.serializers import UserSerializer

class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        users = User.objects.get(pk=pk)
        serializer = UserSerializer(users)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=500)


    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"message": "Deleted successfully"})
