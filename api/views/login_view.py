from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user_serializer import UserSerializer
from api.services.user_service import User
from sabaibiometrics import settings


class LoginView(APIView):
    def post(self, request):
        if not settings.OFFLINE:
            return Response(
                {"error": "Login is disabled in online mode"},
                status=status.HTTP_403_FORBIDDEN,
            )
        emailOrUsername = request.data.get("emailOrUsername")
        try:
            user = User.objects.get(username=emailOrUsername) or User.objects.get(
                email=emailOrUsername
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user is not None:
            return Response(
                {"message": "Login successful", "user": UserSerializer(user).data},
                status=status.HTTP_200_OK,
            )
