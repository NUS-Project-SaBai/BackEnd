from functools import wraps
from rest_framework.response import Response


def require_authentication(view_func):
    """
    Decorator to check if user is authenticated.
    Returns 401 error if not authenticated.
    """

    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
        return view_func(self, request, *args, **kwargs)

    return wrapper


def require_admin(view_func):
    """
    Decorator to check if user is authenticated AND has admin role.
    Returns 401 if not authenticated, 403 if not admin.
    """

    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        if getattr(request.user, "role", "member") != "admin":
            return Response(
                {"error": "Only admin users can perform this action"}, status=403
            )
        return view_func(self, request, *args, **kwargs)

    return wrapper


def require_role(required_role):
    """
    Decorator factory to check if user has a specific role.
    Usage: @require_role("admin")

    Args:
        required_role: The role required to access the view
    """

    def wrapper(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required"}, status=401)

            user_role = getattr(request.user, "role", "member")
            if user_role != required_role:
                return Response(
                    {"error": f"This action requires {required_role} role"}, status=403
                )
            return view_func(self, request, *args, **kwargs)

        return wrapper

    return wrapper
