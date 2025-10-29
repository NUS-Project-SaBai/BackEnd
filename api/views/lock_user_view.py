from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services import user_service
from api.serializers import UserSerializer


class LockUserView(APIView):
    """
    Endpoint for locking user accounts.
    POST /api/users/{username}/lock/
    """

    def post(self, request, username):
        """Lock a user account."""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response({"error": "Only admin users can lock accounts"}, status=403)

        user = user_service.filter_users(username=username).first()

        if not user:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            updated_user = user_service.update_user_with_auth0(
                user, {"is_locked": True}
            )
            return Response(
                {
                    "message": "Account locked successfully",
                    "user": UserSerializer(updated_user).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to lock account: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
