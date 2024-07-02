from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exc, context)
    print(exc)

    # Now add the HTTP status code to the response.
    if isinstance(exc, ObjectDoesNotExist):
        return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, ValueError):
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    elif response is None:
        return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response