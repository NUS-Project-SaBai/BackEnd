"""
Custom API Client with automatic error response validation
"""

from rest_framework.test import APIClient
from rest_framework.response import Response


class CustomAPIClient(APIClient):
    """
    Extended APIClient that validates error responses contain expected fields
    """

    REQUIRED_ERROR_FIELD = "error"  # Enforces "error" key in all error responses

    def _validate_error_response(self, response: Response):
        """
        Validate that error responses contain required fields
        """
        # Skip validation when empty/falsey string is used
        if not getattr(self, "REQUIRED_ERROR_FIELD", None):
            return

        if 400 <= response.status_code < 600:
            # Check if response has data
            if not hasattr(response, "data"):
                raise AssertionError(
                    f"Error response (status {response.status_code}) has no data attribute"
                )

            field = self.REQUIRED_ERROR_FIELD
            if field not in response.data:
                raise AssertionError(
                    f"Error response (status {response.status_code}) missing required field: '"
                    f"{field}'. Response data: {response.data}",
                )

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def put(self, *args, **kwargs):
        response = super().put(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def patch(self, *args, **kwargs):
        response = super().patch(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        self._validate_error_response(response)
        return response
