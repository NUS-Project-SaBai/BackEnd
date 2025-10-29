from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class Auth0JWTAuthentication(JSONWebTokenAuthentication):
    """
    Custom JWT authentication that looks up users by auth0_id field
    instead of username field.
    """

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id (sub claim).
        Looks up by auth0_id field instead of username.
        """
        auth0_id = payload.get("sub")

        if not auth0_id:
            msg = "Invalid payload: missing sub claim"
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(auth0_id=auth0_id, is_active=True)
        except User.DoesNotExist:
            msg = f"User not found for auth0_id: {auth0_id}"
            raise exceptions.AuthenticationFailed(msg)

        return user
