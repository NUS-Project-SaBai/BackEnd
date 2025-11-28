import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status, serializers


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exc, context)
    print(type(exc), exc, context, flush=True)

    # Now add the HTTP status code to the response.
    if isinstance(exc, ObjectDoesNotExist):
        return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, ValueError):
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, serializers.ValidationError):
        return Response(
            {"error": readable_codes(exc.get_codes())},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exc, Http404):
        return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
    elif response is None:
        # Unhandled exception: generate a correlation id and log with traceback
        error_id = str(uuid.uuid4())
        try:
            view = context.get("view")
            view_name = (
                getattr(view, "__class__", type(view)).__name__ if view else None
            )
            request = context.get("request")
            path = getattr(request, "path", None)
            method = getattr(request, "method", None)
            logger.exception(
                f"Unhandled exception [{error_id}] at {method} {path} in {view_name}"
            )
        except Exception:
            # Fall back to a simple log if context inspection fails
            logger.exception(f"Unhandled exception [{error_id}]")

        return Response(
            {"error": str(exc), "error_id": error_id},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


code_names = {
    "null": "Missing",
    "invalid": "Invalid",
    "required": "Missing",
    "incorrect_type": "Invalid",
    "does_not_exist": "Cannot find",
    "not_found": "Cannot find",
}


def readable_codes(codes) -> str:
    # codes: {"name": ["required"]}
    if isinstance(codes, list):
        return [readable_codes(code) for code in codes]
    elif isinstance(codes, dict):
        return "; ".join(
            [
                ",".join(readable_codes(value)) + " " + key
                for key, value in codes.items()
            ]
        )
    else:
        if codes in code_names:
            return code_names[codes]
        return str(codes.title())
