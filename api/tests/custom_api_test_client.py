"""
Custom API Client with automatic error response validation
"""

from rest_framework.test import APIClient
from rest_framework.response import Response


class CustomAPITestClient(APIClient):
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
        self._ensure_multipart_for_files(args, kwargs)
        response = super().post(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def put(self, *args, **kwargs):
        self._ensure_multipart_for_files(args, kwargs)
        response = super().put(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def patch(self, *args, **kwargs):
        self._ensure_multipart_for_files(args, kwargs)
        response = super().patch(*args, **kwargs)
        self._validate_error_response(response)
        return response

    def _ensure_multipart_for_files(self, args, kwargs):
        """If the request payload contains file-like objects, set
        `format='multipart'` so DRF test client encodes the request
        correctly. This centralizes detection logic used by POST/PUT/PATCH.
        """
        data = kwargs.get("data", None)
        if data is None and len(args) >= 2:
            data = args[1]

        try:
            from django.core.files.uploadedfile import UploadedFile

            has_file = False
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, UploadedFile) or hasattr(v, "read"):
                        has_file = True
                        break
            if has_file and "format" not in kwargs:
                kwargs["format"] = "multipart"
        except Exception:
            # Fail silently; test can still set format explicitly
            pass

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        self._validate_error_response(response)
        return response
