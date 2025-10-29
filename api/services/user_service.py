from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.utils.auth0_utils import (
    create_auth0_user,
    update_auth0_user,
    delete_auth0_user,
)
from api.serializers import UserSerializer

User = get_user_model()


def list_users():
    return User.objects.all().order_by("nickname")


def filter_users(**filters):
    return User.objects.filter(**filters).order_by("nickname")


def get_user(pk):
    return get_object_or_404(User, pk=pk)


def create_user_with_auth0(user_data):
    """
    Create a user in both Auth0 and the local database.

    Args:
        user_data: Dictionary with username, nickname, email, password, role

    Returns:
        tuple: (user, error) - user object if successful, error message if failed
    """
    username = user_data.get("username")
    nickname = user_data.get("nickname", username)
    email = user_data.get("email")
    password = user_data.get("password")
    role = user_data.get("role", "member")

    # Validate required fields
    if not username or not email or not password:
        return None, "Username, email or password is missing"

    # Create user in Auth0
    try:
        auth0_response = create_auth0_user(username, nickname, email, password, role)
        auth0_id = auth0_response.get("user_id")
        if not auth0_id:
            return None, "Auth0 did not return a user_id"
    except Exception as e:
        return None, f"Failed to create user in Auth0: {str(e)}"

    # Create user in local database
    data = user_data.copy()
    data["auth0_id"] = auth0_id
    serializer = UserSerializer(data=data)

    if not serializer.is_valid():
        # If local creation fails, we should ideally delete from Auth0
        # but for now just return the error
        return None, serializer.errors

    user = serializer.save()
    return user, None


def create_user(validated_data):
    """Create a user directly (for internal use or migrations)"""
    return User.objects.create(**validated_data)


def update_user_with_auth0(user, user_data):
    """
    Update a user in both the local database and Auth0.

    Args:
        user: User instance to update
        user_data: Dictionary with fields to update

    Returns:
        User object
    """
    serializer = UserSerializer(user, data=user_data, partial=True)
    serializer.is_valid(raise_exception=True)

    auth0_id = user.auth0_id
    if not auth0_id:
        raise Exception("Error updating user: missing auth0_id")

    # Update Auth0 with validated data (only fields that changed)
    data = {
        k: v
        for k, v in serializer.validated_data.items()
        if getattr(user, k, None) != v
    }
    if user_data.get("password"):
        data["password"] = user_data["password"]
    update_auth0_user(auth0_id, **data)

    updated_user = serializer.save()
    return updated_user


def update_user(user, validated_data):
    """Update a user directly (for internal use)"""
    for attr, value in validated_data.items():
        setattr(user, attr, value)
    user.save()
    return user


def delete_user_with_auth0(user):
    """
    Delete a user from both Auth0 and the local database.

    Args:
        user: User instance to delete
    """
    auth0_id = user.auth0_id
    if auth0_id:
        try:
            delete_auth0_user(auth0_id)
        except Exception as e:
            print(f"Failed to delete user from Auth0: {str(e)}")
            raise e

    user.delete()


def delete_user(user):
    """Delete a user directly (for internal use)"""
    user.delete()
