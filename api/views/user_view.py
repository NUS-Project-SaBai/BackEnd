from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from api.utils.auth0_utils import create_auth0_user, update_auth0_user, delete_auth0_user


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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = request.data.get("email")
            password = request.data.get("password")
            role = request.data.get("role", "member")
            try:
                auth0_response = create_auth0_user(email, password, role)
                print("Auth0 user created:", auth0_response)
            except Exception as e:
                print("Auth0 user creation failed:", str(e))
        else:
                print("Missing email or password. Skipped Auth0 creation.")            
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            auth0_id = getattr(user, "auth0_id", None)
            role = request.data.get("role")
        if auth0_id and role:
            try:
                update_auth0_user(auth0_id, role)
                print("Auth0 user updated")
            except Exception as e:
                print("Failed to update Auth0 user:", str(e))
        return Response(serializer.data)

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        auth0_id = getattr(user, "auth0_id", None)
        if auth0_id:
            try:
                success = delete_auth0_user(auth0_id)
                if success:
                    print("Auth0 user deleted")
                else:
                    print("Auth0 deletion returned non-success")
            except Exception as e:
                print("Failed to delete user from Auth0:", str(e))
        user.delete()
        return Response({"message": "Deleted successfully"})
