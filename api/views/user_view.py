from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from api.serializers import UserSerializer
from api.utils.auth0_utils import (
    create_auth0_user,
    update_auth0_user,
    delete_auth0_user,
)
from api.services import user_service

User = get_user_model()


class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            user = user_service.get_user(pk)
            return Response(UserSerializer(user).data)

        users = user_service.list_users()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

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
            return Response(
                {"error": f"Failed to create user in Auth0: {str(e)}"}, status=500
            )

        data = request.data.copy()
        data["auth0_id"] = auth0_id
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = user_service.create_user(serializer.validated_data)
        return Response(UserSerializer(user).data)

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

        user = user_service.get_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = user_service.update_user(user, serializer.validated_data)

        auth0_id = updated_user.auth0_id
        role = request.data.get("role")
        if auth0_id and role:
            try:
                update_auth0_user(auth0_id, role)
                print("Auth0 user updated")
            except Exception as e:
                print("Failed to update Auth0 user:", str(e))

        return Response(UserSerializer(updated_user).data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

        user = user_service.get_user(pk)
        auth0_id = user.auth0_id
        if auth0_id:
            try:
                if delete_auth0_user(auth0_id):
                    print("Auth0 user deleted")
                else:
                    print("Auth0 deletion returned non-success")
            except Exception as e:
                print("Failed to delete user from Auth0:", str(e))

        user_service.delete_user(user)
        return Response({"message": "Deleted successfully"})
