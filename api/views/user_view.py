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
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response({"error": "Only admin users can perform this action"}, status=403)

        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "member")
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)
        try:
            auth0_response = create_auth0_user(email, password, role)
            auth0_id = auth0_response.get("user_id")
            if not auth0_id:
                raise Exception("Auth0 did not return a user_id")
        except Exception as e:
            return Response({"error": f"Failed to create user in Auth0: {str(e)}"}, status=500)
        user_data = request.data.copy()
        user_data["auth0_id"] = auth0_id
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response({"error": "Only admin users can perform this action"}, status=403)

        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            auth0_id = user.auth0_id
            role = request.data.get("role")
        if auth0_id and role:
            try:
                update_auth0_user(auth0_id, role)
                print("Auth0 user updated")
            except Exception as e:
                print("Failed to update Auth0 user:", str(e))
        return Response(serializer.data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response({"error": "Only admin users can perform this action"}, status=403)

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
