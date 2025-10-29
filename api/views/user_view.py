from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from api.serializers import UserSerializer
from api.services import user_service

User = get_user_model()


class UserView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            user = user_service.get_user(pk)
            return Response(UserSerializer(user).data)

        users = user_service.filter_users(**request.query_params.dict())
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

        user, error = user_service.create_user_with_auth0(request.data)

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

        user = user_service.get_user(pk)
        updated_user = user_service.update_user_with_auth0(user, request.data)
        return Response(UserSerializer(updated_user).data)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )

        user = user_service.get_user(pk)
        user_service.delete_user_with_auth0(user)
        return Response(
            {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
