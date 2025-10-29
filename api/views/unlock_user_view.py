from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services import user_service
from api.serializers import UserSerializer


class UnlockUserView(APIView):
    """
    Endpoint for unlocking user accounts.
    POST /api/users/{username}/unlock/
    """

    def post(self, request, username):
        """Unlock a user account."""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can unlock accounts"}, status=403
            )

        user = user_service.filter_users(username=username).first()

        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            updated_user = user_service.update_user_with_auth0(
                user, {"is_locked": False}
            )
            return Response(
                {
                    "message": "Account unlocked successfully",
                    "user": UserSerializer(updated_user).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to unlock account: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
